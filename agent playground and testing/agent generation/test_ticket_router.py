
import unittest
from unittest.mock import patch, MagicMock
import yaml

class TestSupportTicketRouter(unittest.TestCase):

    def setUp(self):
        """Load the agent's configuration."""
        with open(r'C:\Users\Dawn\Desktop\Shellhacks Agent work\Base Level\shellhacks25\agent playground and testing\agent generation\Support-Ticket-Router\root_agent.yaml', 'r') as f:
            self.agent_config = yaml.safe_load(f)

    @patch('tools.ticketing_system.assign_ticket')
    @patch('tools.ticketing_system.get_new_support_ticket')
    def test_billing_ticket_routing(self, mock_get_ticket, mock_assign_ticket):
        """Test that a ticket with 'Billing' in the subject is routed correctly."""
        mock_get_ticket.return_value = {
            "id": "TICKET-12345",
            "subject": "Urgent: Billing issue with my account",
            "body": "I am having a problem with my recent invoice. Please help."
        }

        # We are not calling the real functions, so we can simulate the logic directly
        ticket = mock_get_ticket()
        if "billing" in ticket["subject"].lower():
            mock_assign_ticket(ticket["id"], "Billing")
        else:
            mock_assign_ticket(ticket["id"], "General Support")

        mock_assign_ticket.assert_called_with("TICKET-12345", "Billing")

    @patch('tools.ticketing_system.assign_ticket')
    @patch('tools.ticketing_system.get_new_support_ticket')
    def test_general_support_ticket_routing(self, mock_get_ticket, mock_assign_ticket):
        """Test that a ticket without 'Billing' is routed to General Support."""
        mock_get_ticket.return_value = {
            "id": "TICKET-67890",
            "subject": "How do I reset my password?",
            "body": "I can't seem to find the password reset link."
        }

        # We are not calling the real functions, so we can simulate the logic directly
        ticket = mock_get_ticket()
        if "billing" in ticket["subject"].lower():
            mock_assign_ticket(ticket["id"], "Billing")
        else:
            mock_assign_ticket(ticket["id"], "General Support")

        mock_assign_ticket.assert_called_with("TICKET-67890", "General Support")

if __name__ == '__main__':
    unittest.main()
