Given your current SysDesign score of 2/10 and the August deadline, here's a clean, integrated LLD + HLD study plan structured around your project work. Think of it as two parallel tracks that reinforce each other.

***

## The Mental Model First

**HLD = "What and Where"** — You're an architect deciding which buildings to build and how roads connect them. You think in services, databases, APIs, and data flow. [geeksforgeeks](https://www.geeksforgeeks.org/system-design/difference-between-high-level-design-and-low-level-design/)

**LLD = "How and Why"** — You're a contractor specifying the wiring inside each building. You think in classes, interfaces, algorithms, and design patterns. [systemdesignhandbook](https://www.systemdesignhandbook.com/blog/low-level-design-vs-high-level-design/)

In interviews: HLD is asked first (30 min), LLD follows or is separate (45 min). You need both fluently. [dev](https://dev.to/devcorner/hld-vs-lld-the-ultimate-system-design-interview-preparation-guide-2025-54do)

***

## The 12-Week Plan (May → July)

Your project should be your LLD + HLD canvas. Build the same project at both levels simultaneously.

### Phase 1 — LLD Foundations (Weeks 1–4)

**Concepts to Master:**
- SOLID Principles (S, O, L, I, D — one per day, 5 days)
- OOP pillars: Encapsulation, Abstraction, Inheritance, Polymorphism
- Core Design Patterns (10 minimum): Singleton, Factory, Builder, Observer, Strategy, Adapter, Decorator, Command, Proxy, Template Method [geeksforgeeks](https://www.geeksforgeeks.org/system-design/what-is-low-level-design-or-lld-learn-system-design/)
- UML: Class diagrams, Sequence diagrams [dev](https://dev.to/devcorner/hld-vs-lld-the-ultimate-system-design-interview-preparation-guide-2025-54do)

**Practice LLD Problems (build these in Python or Java):**

| Week | LLD Problem | What it teaches |
|------|------------|-----------------|
| 1 | Parking Lot System | OOP, enums, SOLID |
| 2 | Library Management System | Relationships, aggregation |
| 3 | Elevator System | State machine, Strategy pattern |
| 4 | URL Shortener (LLD layer) | Interface design, hashing |

**Daily routine:** 1.5 hrs concept → 1.5 hrs code implementation [scribd](https://www.scribd.com/document/978638644/LLD-HLD-15-Days-Plan)

***

### Phase 2 — HLD Foundations (Weeks 3–7, overlapping)

Start HLD in Week 3 so both tracks develop together. [reddit](https://www.reddit.com/r/leetcode/comments/1ckp2zm/how_much_time_does_it_take_to_learn_system_design/)

**Concepts to Master:**
- CAP Theorem, consistency models
- Load Balancing, Caching (Redis), CDN
- SQL vs NoSQL trade-offs, sharding, replication
- Message Queues (Kafka, RabbitMQ)
- API Gateway, Microservices, Rate Limiting
- Database indexing, partitioning
- Horizontal vs Vertical scaling

**Practice HLD Problems (1 per 2 days):**

| Week | HLD Problem | Core concept |
|------|-------------|--------------|
| 3–4 | Design URL Shortener | Hashing, DB choice, scaling |
| 4–5 | Design Twitter Feed | Fan-out, caching, eventual consistency |
| 5–6 | Design WhatsApp | WebSockets, message queues, storage |
| 6–7 | Design Uber/Ola | Geo-sharding, real-time matching |

***

### Phase 3 — Project Integration + Mock Interviews (Weeks 8–12)

This is where you convert knowledge into confidence — your Comcast win pattern. [testrigor](https://testrigor.com/blog/high-level-design-hld-vs-low-level-design-lld/)

**Your Project (pick one to build end-to-end):**
- **Recommended:** A **URL Shortener + Analytics** microservice in Python/Clojure
- It's small enough to fully implement, but rich enough to demonstrate both HLD (load balancer, Redis cache, DB choice) and LLD (clean classes, interfaces, design patterns)

**Weekly rhythm:**
- 2 days: HLD mock (whiteboard a full system in 30 min with explanation out loud)
- 2 days: LLD mock (design + code a module in 45 min)
- 1 day: Review and refine the project based on gaps found

***

## Resources (Ranked by Speed-to-Value)

| Resource | Use For | Priority |
|----------|---------|----------|
| [Algomaster.io/learn/lld](https://algomaster.io/learn/lld) | LLD structured path | 🔴 Start now |
| Gaurav Sen (YouTube) | HLD concepts | 🔴 Start Week 3 |
| Refactoring.Guru | Design patterns with visuals | 🟡 LLD reference |
| ByteByteGo book/newsletter | HLD systems | 🟡 HLD reference |
| Grokking System Design | Interview-format practice | 🟢 Weeks 6–12 |

***

## The Confidence Bridge

You already know this from Comcast: **confident communication > perfect answer**.  For every design problem you practice, do this: [systemdesignhandbook](https://www.systemdesignhandbook.com/blog/low-level-design-vs-high-level-design/)

1. **State assumptions out loud** before designing (buys time, shows structure)
2. **Narrate your trade-offs** ("I chose Redis here because reads are 10x more frequent than writes")
3. **Ask one clarifying question** before drawing anything — interviewers reward this

Practice this narration ritual daily even on paper problems. It turns knowledge into performance.

***

## Weekly Time Budget

Given your energy constraints (family draining), protect your **8:30 AM + post-cold shower** peak window:

- **Mon–Fri:** 8:30–11:30 AM = 3 hrs focused (2 concept + 1 code/practice)
- **Sat:** Full mock interview simulation (HLD + LLD back to back, 90 min)
- **Sun:** Review + project work only, no new concepts

This gives you ~18 hrs/week, enough to complete both tracks by late July with buffer for mock interviews in August. [reddit](https://www.reddit.com/r/leetcode/comments/1ckp2zm/how_much_time_does_it_take_to_learn_system_design/)

Which project are you currently working on? Share the details so I can map the LLD + HLD exercises directly onto it.