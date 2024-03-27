"""
This module provides a class for representing an excess of loss treaty.
"""
from dataclasses import dataclass


@dataclass
class ExcessOfLoss:
    """Class representing an excess of loss treaty."""

    deductible: float
    limit: float
    aad: float = None
    aal: float = None

    def __post_init__(self):
        """Initialize additional attributes after object creation."""
        self.total_recoveries = 0.0
        self.claim_amount_in_excess = 0.0
        self.available_aad = self.aad
        self.recoveries = 0.0

    def apply_treaty(self, claim_amount):
        """Apply the excess of loss treaty to a claim amount.

        Args:
            claim_amount (float): The claim amount to which the treaty is applied.

        Returns:
            ExcessOfLoss: The updated ExcessOfLoss object after applying the treaty.
        """
        self.claim_amount_in_excess = max(claim_amount - self.deductible, 0)

        if self.claim_amount_in_excess == 0:
            self.recoveries = 0
            return self

        if self.aad:
            aad = self.available_aad
            self.available_aad = max(aad - self.claim_amount_in_excess, 0)
            self.claim_amount_in_excess = max(
                self.claim_amount_in_excess - aad, 0)

        recoveries = min(self.claim_amount_in_excess, self.limit)

        if self.aal:
            available_recovery = self.aal - self.total_recoveries
            recoveries = min(recoveries, available_recovery)
            self.total_recoveries += recoveries

        self.recoveries = recoveries
        return self

@dataclass
class QuotaShare:
    """Class representing a quota share treaty."""

    share: float  # The reinsurer's share of premiums and losses, expressed as a decimal.

    def __post_init__(self):
        """Initialize additional attributes after object creation."""
        self.recoveries = 0.0

    def apply_treaty(self, claim_amount):
        """Apply the quota share treaty to premiums and losses.

        Args:
            premium (float): The premium amount to be shared.
            loss (float): The loss amount to be shared.

        Returns:
            QuotaShare: The updated QuotaShare object after applying the treaty.
        """
        self.recoveries = claim_amount * self.share
        return self

treaties_map = {'xs': ExcessOfLoss, 'qs': QuotaShare}

