import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from reelkit import *
Q = "Last year, I ___ to London."
QO = ["A. have been", "B. went"]
REELS = {
 "2026-11-25-discuss": [
    intro("IELTS Writing tip", "Stop writing this", "in your essays", "(examiners notice it)", "mistake"),
    wrong("“discuss about”"),
    right("“discuss”", "“Discuss” already means “talk about”.", "No “about” needed."),
    items("Say it like this", ["Let’s discuss the plan.", "This essay discusses two views.", "We discussed the problem."]),
    outro("for your next essay"),
 ],
 "2026-11-26-very-important": [
    intro("Vocabulary upgrade", "Stop saying", "“very important”", "Try these for a higher band", "vocab"),
    wrong("“very important”", label="Too basic"),
    items("Say this instead", ["crucial", "essential", "vital"], big=True),
    right("“Sleep is essential.”", "Same meaning, stronger word.", "Great for IELTS Writing and Speaking."),
    outro("for your IELTS exam"),
 ],
 "2026-11-27-quiz-went": [
    intro("Quick quiz", "Which one is", "correct?", "Comment your answer", "quiz"),
    quiz(Q, QO),
    quiz_reveal(Q, QO, 1, "“Last year” = finished time,", "so use the past simple: “went”."),
    outro("before your next test"),
 ],
 "2026-11-28-i-think": [
    intro("IELTS Speaking tip", "Stop starting", "with “I think…”", "Sound more natural", "speaking"),
    wrong("“I think…”", label="Overused"),
    items("Try these instead", ["In my opinion, …", "From my perspective, …", "I’d say that …"]),
    right("“I’d say that…”", "Relaxed, natural and fluent.", "Perfect for Speaking Part 1."),
    outro("for your speaking test"),
 ],
}
