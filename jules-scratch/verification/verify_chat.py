from playwright.sync_api import sync_playwright, expect
import os
import json

def verify_chat_client():
    """
    This script verifies the functionality of the chat_client.html file.
    It connects to the WebSocket server, sends a message, and captures a screenshot.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Get the absolute path to the HTML file to ensure it can be found
        file_path = os.path.abspath("chat_client.html")

        # Navigate to the local HTML file
        page.goto(f"file://{file_path}")

        # Click the connect button to establish the WebSocket connection
        page.locator("#connectButton").click()

        # Wait for the status to update to "Connected"
        expect(page.locator("#status")).to_have_text("Connected")

        # Verify that the "Connected to server" message appears
        expect(page.locator("#messages li").first).to_have_text("Connected to server.")

        # Prepare a test message to send to the server
        test_message = {
            "command": "create_persona",
            "payload": {
                "name": "Test Persona",
                "alias": "The Tester",
                "universe": "Testverse",
                "spawned_from": "Verification Script",
                "traits": ["Automated", "Reliable"],
                "purpose": "To verify the chat server.",
                "parable": "A test persona is born."
            }
        }

        # Fill the input field with the JSON message
        page.locator("#input").fill(json.dumps(test_message))

        # Click the send button
        page.get_by_role("button", name="Send").click()

        # Verify that the sent message appears in the chat log
        expect(page.locator("#messages li").nth(1)).to_have_text(f"You: {json.dumps(test_message)}")

        # Wait for the server's response and verify it indicates success
        expect(page.locator("#messages li").nth(2)).to_contain_text('"status":"success"')

        # Take a screenshot to visually confirm the result
        page.screenshot(path="jules-scratch/verification/verification.png")

        print("Verification script completed successfully and screenshot taken.")
        browser.close()

if __name__ == "__main__":
    verify_chat_client()