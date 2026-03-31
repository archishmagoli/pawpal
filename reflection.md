# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
I centered my design around the core user actions necessary for the application. In this case, a user should be able to perform the following actions:
- Add pet information
- Schedule tasks (e.g. walk the pet, bath time, etc.)
- View the daily schedule of tasks

- What classes did you include, and what responsibilities did you assign to each?

I believe the application should have the following classes and associated attributes/methods. In general, the `Task` class holds the associated methods for creating a task, and each `Pet` will have a list of tasks it needs to get done on its behalf:
### `Owner`
- **Attributes:** `name`, `pets: list[Pet]`, `available_time: int` (minutes/day)
- **Methods:** `add_pet(pet)`, `remove_pet(name)`, `get_pet(name)`

### `Pet`
- **Attributes:** `name`, `age`, `species`, `tasks: list[Task]`
- **Methods:** `add_task(task)`, `remove_task(name)`, `get_tasks()`

### `Task`
- **Attributes:** `name`, `duration: int` (minutes), `priority: str`, `category: str`, `start_time: str | None`
- **Methods:** none — plain data object

### `Schedule`
- **Attributes:** `date`, `pet: Pet`, `available_time: int`, `tasks: list[Task]`
- **Methods:** `generate_plan()`, `display_plan()`

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, my design **did change** during implementation. When I let Claude (via Copilot) take the reins in class design once I had given it a rough idea of what classes, methods, and attributes I was looking for, Claude suggested having **five** classes, with the additional fifth class being for `ScheduledTask`s. I felt this was somewhat redundant, since we already had a `Task` class we could just expand during scheduling, so I suggested we remove that class and stick with the four we have above. Additionally, I initially had each `Owner` own the list of tasks generated, but then that would be difficult to categorize per animal, so I asked Claude to move that ownership to each `Per` instead. This allows for categorization while still allowing us to group by `Owner` via the `Owner has multiple Pets` relationship.

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
