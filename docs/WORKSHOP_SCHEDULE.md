# Workshop Schedule

## Full Day Workshop (6 hours)

### Morning Session (3 hours)

#### 09:00 - 09:30 | Setup & Introduction (30 min)
- ✅ Welcome and objectives
- ✅ Environment setup verification
- ✅ GitHub Copilot introduction
- ✅ Repository tour
- ✅ Q&A

**Activities**:
- Clone repository
- Verify Go/Python installations
- Test Copilot is working
- Review project structure

---

#### 09:30 - 10:15 | Demo Conversion (45 min)
**Instructor demonstrates converting URL Shortener module**

**Topics Covered**:
1. Reading and understanding Go source code (5 min)
2. Setting up Python project structure (5 min)
3. Converting models (structs → Pydantic) (10 min)
4. Converting storage interface (10 min)
5. Converting one handler (10 min)
6. Copilot techniques showcase (5 min)

**Copilot Features Demonstrated**:
- Comment-driven development
- Inline suggestions
- Copilot Chat usage
- `/tests` command
- `/doc` command
- `/fix` command

---

#### 10:15 - 10:30 | Break (15 min)
☕ Coffee break

---

#### 10:30 - 12:00 | Hands-On Part 1 (90 min)
**Participants work on chosen applications**

**Checkpoints**:
- [ ] Project setup complete (20 min)
- [ ] Models converted (30 min)
- [ ] Storage/repository layer started (40 min)

**Support**:
- Instructor circulates
- Troubleshooting assistance
- Tips sharing

---

### Lunch Break

#### 12:00 - 13:00 | Lunch (60 min)
🍽️ Lunch break

---

### Afternoon Session (3 hours)

#### 13:00 - 15:00 | Hands-On Part 2 (120 min)
**Continue conversion work**

**Checkpoints**:
- [ ] Storage/repository layer complete (30 min)
- [ ] Business logic converted (45 min)
- [ ] API/CLI layer converted (45 min)

**Milestones**:
- 13:30 - Quick check-in (5 min)
- 14:00 - Mid-afternoon check-in (5 min)
- 14:30 - Progress review (5 min)

---

#### 15:00 - 15:15 | Break (15 min)
☕ Coffee break

---

#### 15:15 - 15:45 | Hands-On Part 3 (30 min)
**Finishing touches**

**Tasks**:
- [ ] Tests conversion and validation
- [ ] Documentation generation
- [ ] Final debugging
- [ ] README updates

---

#### 15:45 - 16:15 | Review & Best Practices (30 min)

**Activities**:
1. Code review showcase (10 min)
   - Volunteers share conversions
   - Discuss interesting challenges

2. Best practices discussion (10 min)
   - What worked well with Copilot
   - Common pitfalls encountered
   - Tips for future conversions

3. Comparison and insights (10 min)
   - Language differences
   - Performance considerations
   - When to convert and when not to

---

#### 16:15 - 16:30 | Q&A and Wrap-up (15 min)

**Topics**:
- Open questions
- Next steps suggestions
- Resource recommendations
- Feedback collection

**Takeaways**:
- Completed (or near-completed) conversion
- Copilot skills learned
- Understanding of cross-language patterns
- Portfolio piece

---

## Half-Day Workshop (3 hours)

### Compressed Schedule

#### Time | Activity | Duration
09:00 - 09:15 | Setup & Introduction | 15 min
09:15 - 09:45 | Demo Conversion (abbreviated) | 30 min
09:45 - 11:15 | Hands-On Conversion | 90 min
11:15 - 11:30 | Break | 15 min
11:30 - 11:50 | Continue Conversion | 20 min
11:50 - 12:00 | Review & Wrap-up | 10 min

**Focus**: One simpler application (URL Shortener or Weather CLI)

---

## Self-Paced Option

### Week 1: Preparation
- [ ] Setup environment
- [ ] Read all documentation
- [ ] Choose application
- [ ] Review source code

### Week 2-3: Conversion
- [ ] Follow IMPLEMENTATION_PLAN.md
- [ ] Track progress in WORKSHOP_PROGRESS.md
- [ ] Complete conversion
- [ ] Test thoroughly

### Week 4: Polish
- [ ] Documentation
- [ ] Performance testing
- [ ] Deploy (optional)
- [ ] Write blog post (optional)

---

## Time Estimates by Application

| Application | Setup | Models | Storage | Logic | API/CLI | Tests | Docs | Total |
|------------|-------|--------|---------|-------|---------|-------|------|-------|
| **URL Shortener** | 15m | 20m | 30m | 30m | 30m | 25m | 10m | **2.5h** |
| **Weather CLI** | 15m | 20m | 25m | 35m | 30m | 25m | 10m | **2.5h** |
| **Blog API** | 20m | 30m | 40m | 45m | 45m | 35m | 15m | **3.5h** |
| **Web Scraper** | 20m | 25m | 35m | 50m | 40m | 35m | 15m | **3.5h** |

*Times are estimates and may vary based on experience level*

---

## Checkpoints for Instructors

### Before Workshop
- [ ] Test all source applications work
- [ ] Verify Copilot suggestions quality
- [ ] Prepare demo conversion
- [ ] Setup example solutions (hidden branch)
- [ ] Test all setup instructions
- [ ] Prepare troubleshooting guide

### During Workshop
- [ ] Monitor participant progress
- [ ] Identify common issues
- [ ] Share tips in real-time
- [ ] Adjust pace as needed
- [ ] Collect questions for Q&A

### After Workshop
- [ ] Collect feedback
- [ ] Review completion rates
- [ ] Identify improvements
- [ ] Update materials
- [ ] Share resources with participants

---

## Tips for Success

### For Participants
1. ⏰ Don't rush - quality over speed
2. 🤝 Ask for help when stuck
3. 💬 Share interesting Copilot discoveries
4. ✅ Test after each module
5. 📝 Take notes on challenges
6. 🎯 Focus on learning, not just completing

### For Instructors
1. 👀 Monitor the room regularly
2. 💡 Share tips proactively
3. 🎪 Make demos engaging
4. 🔧 Be ready to troubleshoot quickly
5. 📢 Keep energy up
6. ⏱️ Stay on schedule (but be flexible)

---

## Emergency Schedule Adjustments

### If Running Behind
- Skip intermediate checkpoints
- Reduce Q&A time
- Provide reference implementation
- Focus on core features only
- Skip advanced features

### If Running Ahead
- Add refactoring exercises
- Discuss performance optimizations
- Try converting additional modules
- Explore advanced Copilot features
- Start second application

---

## Post-Workshop Continuation

### Optional Challenges
1. Complete remaining features
2. Add extra functionality
3. Convert another application
4. Optimize performance
5. Deploy to production
6. Write blog post about experience
7. Create video tutorial
8. Contribute improvements to workshop

### Follow-Up Sessions (Optional)
- Week 2: Show & Tell (30 min)
- Week 4: Advanced Patterns (60 min)
- Week 6: Production Deployment (60 min)
