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

Yes, after further reviewing, my design did change from what the AI model initially proposed. One big change was the addition of an ID charactertistic to the task class. This was a good idea to add because the individual tasks have no other identifiers besides their names, but that could have potential overlap present which might interfere with intended functionality.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

Essentially, the algorithm is using a knapsack fitting. The simplification proposed by the AI model was that we use a 1D table instead of a 2D one, so drop memory used from O(n * capacity) to O(capacity). This is great optimization, but the tradeoff is that readability on the backend does suffer. Still, it's not a huge issue once you're able to figure out the "iterate backwards to avoid reusing an item twice" trick.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

Brainstorming as well as determining what algorithm to use (knapsack fitting) as well as implementing things properly and performing check were what the AI assistant was most helpful in.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When the AI initially started working on this project, it immediately began trying to implement things on it's own and complete the project as fast as possible. So my approach was to tailor my prompts specifically to the task I wanted done and for that to be made clear in my prompt itself.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

The key functionality of this app relies on the correctness in scheduling, determining priority of tasks, and dealing with things like recurrence and/or overlapping of tasks. The AI agent was able to create necessary tests to be certain the functionality of these features was as intended,

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am fairly confident that our scheduler works correctly. Throughout the timeline of working through this project, there were multiple instances where we paused from writing more code or prompting more implementation to instead try to make sure what we had at the moment is not broken in any way, and if there are any loose ends that need to be tied up. Therefore, I think the app should work quite well to at least some degree.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I was satisfied with how smooth most of the process was in terms of the AI agent not having much trouble decoding the requirements, restrictions, and what the user asked for to be done.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, my time would most likely go towards improving the UI/UX system and adding a better visual appeal to our app.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

A key takeaway I had from working with AI on this project and designing systems was that it's really important in OOP to understand how your objects interact with one another and what methods and attributes are responsible for what functionality. The idea of creating so many files seems intimidating but it is actually a really nice way to break the big thing down into smaller problems.
