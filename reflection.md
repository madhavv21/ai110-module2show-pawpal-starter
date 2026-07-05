# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

For my initial idea, I thought up that I should go with four classes to complete this assignment. These four classes are: User, Pet, Task, Schedule/Plan. I think the user and pet classes should be responsible for storing information about the owner and pet respectively. An object of the Task Class would be created whenever a user adds a new task, and it would have attributes such as duration and priority at least. As for the Schedule/Plan Class, it most likely will end up holding data about the overall scheduling the user has done and statuses such as task priorities and the list of tasks itself.

class User: attributes like name, age, dob, num of pets, etc (other basic info). methods like getters/setters etc as needed
class Pet: attributes like name, age, etc (other basic info). methods like getters/setters etc as needed
class Task: an object of type Task created when user adds new task. attributes like task name, duration, priority, time etc. methods like getters/setters etc as necessary
class Schedule: attributes like a list of Task objects. ability to change priorities and/or modify schedules as a whole most likely lies here as well.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
