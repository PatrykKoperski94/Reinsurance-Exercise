"""
This module provides a class for testing the ExcessOfLoss class.
"""
import unittest
from reinsurance import ExcessOfLoss # pylint: disable=import-error


class ExcessOfLossTests(unittest.TestCase):
    """Test cases for the ExcessOfLoss class."""

    def test_apply_treaty_no_aad_aal(self):
        """Test applying the treaty without AAD and AAL."""
        excess_loss = ExcessOfLoss(deductible=1e6, limit=10e6)
        excess_loss.apply_treaty(5e6)
        self.assertEqual(excess_loss.claim_amount_in_excess, 4e6)
        self.assertEqual(excess_loss.recoveries, 4e6)

        excess_loss.apply_treaty(8e6)
        self.assertEqual(excess_loss.claim_amount_in_excess, 7e6)
        self.assertEqual(excess_loss.recoveries, 7e6)

    def test_apply_treaty_limit_saturation_no_aad_aal(self):
        """Test applying the treaty with limit saturation, without AAD and AAL."""
        excess_loss = ExcessOfLoss(deductible=1e6, limit=10e6)
        excess_loss.apply_treaty(15e6)
        self.assertEqual(excess_loss.claim_amount_in_excess, 14e6)
        self.assertEqual(excess_loss.recoveries, 10e6)

        excess_loss.apply_treaty(8e6)
        self.assertEqual(excess_loss.claim_amount_in_excess, 7e6)
        self.assertEqual(excess_loss.recoveries, 7e6)

    def test_apply_treaty_below_deductible_no_aad_aal(self):
        """Test applying the treaty below the deductible, without AAD and AAL."""
        excess_loss = ExcessOfLoss(deductible=1e6, limit=10e6)
        excess_loss.apply_treaty(1)
        self.assertEqual(excess_loss.claim_amount_in_excess, 0)
        self.assertEqual(excess_loss.recoveries, 0)

        excess_loss.apply_treaty(8e6)
        self.assertEqual(excess_loss.claim_amount_in_excess, 7e6)
        self.assertEqual(excess_loss.recoveries, 7e6)

    # AAD
    def test_apply_treaty_with_aad(self):
        """Test applying the treaty with AAD."""
        excess_loss = ExcessOfLoss(deductible=1e6, limit=10e6, aad=2e6)
        excess_loss.apply_treaty(5e6)
        self.assertEqual(excess_loss.claim_amount_in_excess, 2e6)
        self.assertEqual(excess_loss.recoveries, 2e6)
        self.assertEqual(excess_loss.available_aad, 0)

        excess_loss.apply_treaty(8e6)
        self.assertEqual(excess_loss.claim_amount_in_excess, 7e6)
        self.assertEqual(excess_loss.recoveries, 7e6)

    def test_apply_treaty_limit_saturation_with_aad(self):
        """Test applying the treaty with limit saturation, with AAD."""
        excess_loss = ExcessOfLoss(deductible=1e6, limit=10e6, aad=2e6)
        excess_loss.apply_treaty(15e6)
        self.assertEqual(excess_loss.claim_amount_in_excess, 12e6)
        self.assertEqual(excess_loss.recoveries, 10e6)
        self.assertEqual(excess_loss.available_aad, 0)

        excess_loss.apply_treaty(8e6)
        self.assertEqual(excess_loss.claim_amount_in_excess, 7e6)
        self.assertEqual(excess_loss.recoveries, 7e6)

    def test_apply_treaty_below_deductible_with_aad(self):
        """Test applying the treaty below the deductible, with AAD."""
        excess_loss = ExcessOfLoss(deductible=1e6, limit=10e6, aad=2e6)
        excess_loss.apply_treaty(1)
        self.assertEqual(excess_loss.claim_amount_in_excess, 0)
        self.assertEqual(excess_loss.recoveries, 0)
        self.assertEqual(excess_loss.available_aad, 2e6)

        excess_loss.apply_treaty(8e6)
        self.assertEqual(excess_loss.claim_amount_in_excess, 5e6)
        self.assertEqual(excess_loss.recoveries, 5e6)

    # AAL
    def test_apply_treaty_with_aal(self):
        """Test applying the treaty with AAL."""
        excess_loss = ExcessOfLoss(deductible=1e6, limit=10e6, aal=15e6)
        excess_loss.apply_treaty(5e6)
        self.assertEqual(excess_loss.claim_amount_in_excess, 4e6)
        self.assertEqual(excess_loss.recoveries, 4e6)
        self.assertEqual(excess_loss.total_recoveries, 4e6)

        excess_loss.apply_treaty(8e6)
        self.assertEqual(excess_loss.claim_amount_in_excess, 7e6)
        self.assertEqual(excess_loss.recoveries, 7e6)
        self.assertEqual(excess_loss.total_recoveries, 11e6)

        excess_loss.apply_treaty(8e6)
        self.assertEqual(excess_loss.claim_amount_in_excess, 7e6)
        self.assertEqual(excess_loss.recoveries, 4e6)
        self.assertEqual(excess_loss.total_recoveries, 15e6)

    def test_apply_treaty_limit_saturation_with_aal(self):
        """Test applying the treaty with limit saturation, with AAL."""
        excess_loss = ExcessOfLoss(deductible=1e6, limit=10e6, aal=15e6)
        excess_loss.apply_treaty(20e6)
        self.assertEqual(excess_loss.claim_amount_in_excess, 19e6)
        self.assertEqual(excess_loss.recoveries, 10e6)
        self.assertEqual(excess_loss.total_recoveries, 10e6)

        excess_loss.apply_treaty(8e6)
        self.assertEqual(excess_loss.claim_amount_in_excess, 7e6)
        self.assertEqual(excess_loss.recoveries, 5e6)
        self.assertEqual(excess_loss.total_recoveries, 15e6)

    def test_apply_treaty_below_deductible_with_aal(self):
        """Test applying the treaty below the deductible, with AAL."""
        excess_loss = ExcessOfLoss(deductible=1e6, limit=10e6, aal=15e6)
        excess_loss.apply_treaty(1)
        self.assertEqual(excess_loss.claim_amount_in_excess, 0)
        self.assertEqual(excess_loss.recoveries, 0)
        self.assertEqual(excess_loss.total_recoveries, 0)

    # AAD & AAL
    def test_apply_treaty_with_aad_aal(self):
        """Test applying the treaty with AAD and AAL."""
        excess_loss = ExcessOfLoss(
            deductible=1e6, limit=10e6, aad=2e6, aal=15e6)
        excess_loss.apply_treaty(5e6)
        self.assertEqual(excess_loss.claim_amount_in_excess, 2e6)
        self.assertEqual(excess_loss.recoveries, 2e6)
        self.assertEqual(excess_loss.available_aad, 0)
        self.assertEqual(excess_loss.total_recoveries, 2e6)


if __name__ == '__main__':
    unittest.main()
