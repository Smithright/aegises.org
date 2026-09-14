"""Selected Qthonic decision functions. See provenance.json; no transport or credentials."""
import uuid
LEASE_TTL_S = 1800

def _int(val, default=0):
    try:
        return int(val)
    except (TypeError, ValueError):
        return default

def lease_of(row):
    """The lease as the row carries it. `fence` is 0 on a never-leased row,
    which is what makes `guard_write` vacuous for all 214 live rows."""
    return {
        "holder": (row.get("lease_holder") or "").strip() or None,
        "claim_id": (row.get("lease_claim_id") or "").strip() or None,
        "fence": _int(row.get("lease_fence"), 0),
        "expiry": _int(row.get("lease_expiry"), 0),
        "attempts": _int(row.get("lease_attempts"), 0),
    }

def fence_verdict(row, presented, now):
    """THE LOAD-BEARING CONTROL. (ok, reason_code, detail).

    Kleppmann's fencing token, at the resource: the holder pauses (GC, VM
    migration, a partition — or, here, a quota stall), the TTL expires, the
    ticket is reclaimed and re-worked, and then the paused holder wakes and
    writes AS THOUGH IT STILL HOLDS THE CLAIM. A lease shortens that window;
    only a monotonic token closes it. The zombie's write is not refused by a
    guard exercising judgement — it is arithmetically invalid.

    The rules, and each one exists because its absence is an escape hatch:

      never leased (fence 0)  + no proof  -> ALLOW. Today's board, untouched.
      never leased            + a proof   -> refuse `no-lease`: nothing ever
                                             issued that token.
      ever leased             + no proof  -> refuse `fence-required`. A check
                                             you evade by omitting a field is
                                             not a check. This is why the
                                             requirement keys on `fence > 0`
                                             (ever leased) and not on a LIVE
                                             lease: between expiry and
                                             reclaim there is no live lease,
                                             and that gap is exactly when the
                                             zombie wakes.
      proof <  row fence      -> refuse `stale-fence`   <-- the zombie
      proof >  row fence      -> refuse `forged-fence`: no such token was
                                             ever minted.
      proof == row fence, lease held but EXPIRED -> refuse `lease-expired`:
                                             the TTL is the point. The holder
                                             gets its refusal from the clock,
                                             not from its own good behaviour.
      proof == row fence, no holder (released/reclaimed) -> ALLOW: the fence
                                             is current, so this writer is
                                             not stale; ownership is Cedar's
                                             question, not the fence's.
      proof == row fence, lease LIVE       -> ALLOW.
    """
    lease = lease_of(row)
    fence = lease["fence"]
    if presented is None:
        if fence <= 0:
            return True, "unleased", ""
        return False, "fence-required", (
            "ticket carries lease fence %d — every write to an ever-leased "
            "row must present it" % fence)
    presented = _int(presented, -1)
    if presented < 0:
        return False, "malformed-fence", "fence must be a non-negative integer"
    if fence <= 0:
        return False, "no-lease", (
            "fence %d presented against a ticket that has never been leased"
            % presented)
    if presented < fence:
        return False, "stale-fence", (
            "fence %d is STALE — the resource has seen %d. The lease was "
            "reclaimed while this writer was away; its work is not current."
            % (presented, fence))
    if presented > fence:
        return False, "forged-fence", (
            "fence %d was never issued — the resource has seen %d"
            % (presented, fence))
    if lease["holder"] and lease["expiry"] <= now:
        return False, "lease-expired", (
            "lease on this ticket expired at %d (now %d); it is awaiting "
            "reclaim" % (lease["expiry"], now))
    return True, "current", ""

def grant(row, holder, now, ttl=None):
    """Mint a lease. (ok, code, detail, patch, lease).

    The fence increments on EVERY grant and EVERY reclaim, so it is
    monotonic per ticket under both paths — a reclaimed ticket already
    invalidates its zombie before anyone re-grants it.

    WIP and exclusivity: a live lease held by anyone refuses a second grant.
    `next()`'s WIP=1 (one open lease per agent, §4.3) belongs to the pull
    loop in S3 and is NOT enforced here; what IS enforced here is the
    per-ticket exclusivity two concurrent claims race for."""
    lease = lease_of(row)
    if lease["holder"] and lease["expiry"] > now:
        if lease["holder"] == holder:
            return (False, "already-held", "you already hold this lease at "
                    "fence %d — renew it, do not re-grant" % lease["fence"],
                    None, lease)
        return (False, "lease-held",
                "held by %s until %d" % (lease["holder"], lease["expiry"]),
                None, lease)
    fence = lease["fence"] + 1
    claim_id = "L-" + uuid.uuid4().hex[:12]
    expiry = now + (ttl if ttl is not None else LEASE_TTL_S)
    patch = {
        "status": "claimed",
        "lease_holder": holder,
        "lease_claim_id": claim_id,
        "lease_fence": fence,
        "lease_expiry": expiry,
        "lease_attempts": lease["attempts"],
        # `principal` keeps meaning last-toucher, exactly as it always has;
        # the lease does not quietly redefine it (#190's whole complaint).
        "principal": holder,
    }
    return True, "granted", "", patch, {
        "claim_id": claim_id, "fence": fence, "expiry": expiry,
        "holder": holder, "ttl": expiry - now}
