#!/usr/bin/env python3
"""
Phishing Awareness Training - interactive command-line module.

This is a defensive awareness exercise. It teaches users to identify
suspicious messages and choose safe responses. It does not send emails,
visit websites, collect credentials, or interact with real accounts.
"""

QUESTIONS = [
    {
        "topic": "Suspicious email",
        "question": "You receive an unexpected email saying your account will close in 10 minutes. It asks you to sign in using a link. What should you do?",
        "options": [
            "A. Click immediately to avoid losing access",
            "B. Do not click; open the official service independently or contact support using a trusted channel",
            "C. Forward it to friends to ask whether it is real",
        ],
        "answer": "B",
        "explanation": "Urgency and unexpected sign-in links are common warning signs. Verify independently."
    },
    {
        "topic": "Sender verification",
        "question": "The sender display name says 'Company IT', but the full email address is unfamiliar. What is safest?",
        "options": [
            "A. Trust the display name",
            "B. Reply with your password to confirm your identity",
            "C. Check the full sender address and verify the request through an approved IT channel",
        ],
        "answer": "C",
        "explanation": "Display names can be misleading. Verify the sender and request through a separate trusted channel."
    },
    {
        "topic": "Fake websites",
        "question": "A website shows a padlock, but its domain is unfamiliar and slightly misspelled. Is it safe?",
        "options": [
            "A. Yes, a padlock proves the site is genuine",
            "B. No. HTTPS protects the connection but does not prove the site is legitimate",
            "C. Yes, if the page looks professional",
        ],
        "answer": "B",
        "explanation": "HTTPS encrypts the connection. It does not establish that the website belongs to the organization it claims to represent."
    },
    {
        "topic": "Social engineering",
        "question": "A caller claiming to be IT support asks you to read out a one-time passcode. What should you do?",
        "options": [
            "A. Share it because they sound professional",
            "B. Refuse and contact IT through your organization's known support channel",
            "C. Send the code by text instead",
        ],
        "answer": "B",
        "explanation": "Never share passwords or one-time codes. Verify unexpected support requests independently."
    },
    {
        "topic": "Unexpected attachment",
        "question": "A colleague sends an unexpected attachment with a vague message. What is the safest next step?",
        "options": [
            "A. Open it to find out what it is",
            "B. Confirm with the colleague through a separate trusted channel before opening it",
            "C. Disable security software so it opens correctly",
        ],
        "answer": "B",
        "explanation": "A colleague's account could be compromised. Confirm unusual files and requests before opening them."
    },
    {
        "topic": "Reporting",
        "question": "You clicked a suspicious link and entered your password. What should you do?",
        "options": [
            "A. Ignore it and hope nothing happens",
            "B. Delete the email and tell nobody",
            "C. Report it immediately, change the password through the official site, and follow your organization's incident process",
        ],
        "answer": "C",
        "explanation": "Fast reporting helps limit harm. If the password was reused, change it on other affected services too."
    },
]

def ask_question(number, item):
    print(f"\nQuestion {number}: {item['topic']}")
    print(item["question"])
    for option in item["options"]:
        print("  " + option)

    while True:
        answer = input("Your answer (A/B/C): ").strip().upper()
        if answer in {"A", "B", "C"}:
            break
        print("Please enter A, B, or C.")

    correct = answer == item["answer"]
    print("Correct!" if correct else f"Not quite. Correct answer: {item['answer']}")
    print("Why:", item["explanation"])
    return correct

def main():
    print("=" * 60)
    print("PHISHING AWARENESS TRAINING")
    print("=" * 60)
    print("Learn to spot suspicious emails, fake websites, and social engineering.")
    print("This local quiz does not collect or transmit your answers.")
    print("\nRemember: STOP - CHECK - REPORT.")
    input("\nPress Enter to begin...")

    score = 0
    for number, item in enumerate(QUESTIONS, start=1):
        if ask_question(number, item):
            score += 1

    total = len(QUESTIONS)
    print("\n" + "=" * 60)
    print(f"Training complete. Your score: {score}/{total}")
    if score == total:
        print("Excellent work! You identified every safe response.")
    elif score >= 4:
        print("Good work. Review the explanations for any missed questions.")
    else:
        print("Keep learning. Review the training notes and try again.")
    print("\nKey habits:")
    print("- Do not click unexpected links or attachments.")
    print("- Verify unusual requests through a separate trusted channel.")
    print("- Never share passwords or one-time codes.")
    print("- Report suspected phishing quickly.")
    print("=" * 60)

if __name__ == "__main__":
    main()
