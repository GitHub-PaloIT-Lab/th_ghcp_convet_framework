# Convert Framework Workshop

> Learn cross-language code conversion with GitHub Copilot

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd convert-framework

# 2. Try a Go application
cd go/url-shortener
go mod download
redis-server &  # Start Redis in background
go run cmd/server/main.go
# → Server at http://localhost:8080

# 3. Try a Python application
cd ../../python/weather-cli
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
python -m weather_cli.cli current "Bangkok"
```

**📱 Quick Commands:**
```bash
make run-url       # Go URL Shortener
make run-blog      # Go Blog API  
make run-weather   # Python Weather CLI
make run-scraper   # Python Web Scraper
```

**📖 App-Specific Guides:**
- [go/url-shortener/README.md](go/url-shortener/README.md)
- [go/blog-api/README.md](go/blog-api/README.md)
- [python/weather-cli/README.md](python/weather-cli/README.md)
- [python/web-scraper/README.md](python/web-scraper/README.md)

---

## Overview

เวิร์กช็อปนี้สอนการใช้ GitHub Copilot ช่วยแปลงโค้ดข้ามภาษา (Go ↔ Python) โดยมีแอพพลิเคชั่นตัวอย่างที่มีความซับซ้อนพอสมควร พร้อม patterns, techniques และ best practices สำหรับการ migrate code อย่างมีประสิทธิภาพ

## Workshop Objectives

เรียนรู้:
- 🤖 ใช้ GitHub Copilot แปลงโค้ดข้ามภาษาอย่างมีประสิทธิภาพ
- 🔄 แปลง language idioms, patterns และ type systems
- 🧪 Migrate tests, dependencies และ configuration
- 📚 Best practices สำหรับ cross-language conversion
- ⚡ เทคนิค prompt engineering สำหรับ AI-assisted coding

## Applications

### Go Applications (แปลงเป็น Python)

1. **URL Shortener API** 🔗
   - REST API สำหรับย่อ URL พร้อม analytics
   - Chi router + Redis + SQLite
   - → Python/FastAPI
   - Complexity: ⭐⭐⭐ (Medium, 2-3 hours)

2. **Blog REST API** 📝
   - Blog platform พร้อม posts, comments, tags
   - Gin + PostgreSQL + JWT
   - → Python/Django REST Framework
   - Complexity: ⭐⭐⭐⭐ (High, 3-4 hours)

### Python Applications (แปลงเป็น Go)

3. **Weather CLI Tool** 🌤️
   - CLI สำหรับดูสภาพอากาศจากหลาย APIs
   - Click + Requests + SQLite
   - → Go/Cobra
   - Complexity: ⭐⭐⭐ (Medium, 2-3 hours)

4. **Web Scraper** 🕷️
   - Configurable scraper พร้อม data export
   - BeautifulSoup4 + Requests + Pandas
   - → Go/Colly + goquery
   - Complexity: ⭐⭐⭐⭐ (High, 3-4 hours)

## Project Structure

```
convert-framework/
├── .github/
│   └── copilot-instructions.md    # Copilot configuration
├── go/                             # Go applications
│   ├── url-shortener/             # URL Shortener (to be created)
│   └── blog-api/                  # Blog API (to be created)
├── python/                         # Python applications
│   ├── weather-cli/               # Weather CLI (to be created)
│   └── web-scraper/               # Web Scraper (to be created)
├── docs/                           # Workshop documentation
│   ├── IMPLEMENTATION_PLAN.md     # Detailed implementation guide
│   ├── APPLICATION_SELECTION.md   # Help choosing an application
│   ├── COPILOT_GUIDE.md          # Copilot techniques & prompts
│   └── WORKSHOP_PROGRESS.md      # Track your progress
└── README.md                       # This file
```

## Getting Started

### Prerequisites

**For All Participants:**
- GitHub Copilot subscription (or trial)
- VS Code with GitHub Copilot extension
- Git installed
- Basic understanding of both Go and Python

**For Go Applications:**
- Go 1.21+ installed
- PostgreSQL (for Blog API)
- Redis (for URL Shortener)

**For Python Applications:**
- Python 3.11+ installed
- pip and virtualenv

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/convert-framework.git
   cd convert-framework
   ```

2. **Setup GitHub Copilot**
   - Install GitHub Copilot extension in VS Code
   - Sign in with your GitHub account
   - Verify Copilot is active (check status bar)

3. **Choose your application**
   - Read [docs/APPLICATION_SELECTION.md](docs/APPLICATION_SELECTION.md)
   - Pick an application based on your interests and time

4. **Read the guides**
   - [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) - Detailed steps
   - [docs/COPILOT_GUIDE.md](docs/COPILOT_GUIDE.md) - Copilot techniques
   - [.github/copilot-instructions.md](.github/copilot-instructions.md) - Conversion patterns

## Workshop Flow

### Module 1: Setup & Introduction (30 min)
1. ✅ Environment setup
2. ✅ Review source applications
3. ✅ Choose conversion path
4. ✅ Review Copilot basics

### Module 2: Demo Conversion (45 min)
**Instructor demonstrates** converting one module from URL Shortener:
- Convert models (structs → Pydantic)
- Convert storage layer
- Convert one handler
- Copilot techniques walkthrough

### Module 3: Hands-On Conversion (90-120 min)
**You work on your chosen application:**
- Follow checkpoints in IMPLEMENTATION_PLAN.md
- Use techniques from COPILOT_GUIDE.md
- Track progress in WORKSHOP_PROGRESS.md
- Ask for help when stuck

### Module 4: Review & Best Practices (30 min)
1. Review completed conversions
2. Discuss challenges
3. Share Copilot tips
4. Q&A

## Conversion Workflow

```mermaid
graph TD
    A[Choose Application] --> B[Read Source Code]
    B --> C[Setup Project Structure]
    C --> D[Convert Models]
    D --> E[Convert Storage/Repository]
    E --> F[Convert Business Logic]
    F --> G[Convert API/CLI Layer]
    G --> H[Convert Tests]
    H --> I[Generate Documentation]
    I --> J[Final Review]
```

## Key Features

### 🤖 AI-Powered Conversion
- Inline suggestions for code translation
- Chat-based explanations and conversions
- Automated test generation
- Documentation generation

### 📚 Comprehensive Guides
- Very detailed implementation plan
- Language-specific prompt templates
- Common patterns and pitfalls
- Real-world examples

### ✅ Progress Tracking
- Structured checklists
- Learning objectives tracking
- Notes and reflections
- Feedback collection

### 🎯 Practical Applications
- Real-world complexity
- Common patterns and frameworks
- Full feature implementations
- Production-ready practices

## Quick Start Commands

### Go Projects

```bash
# URL Shortener
cd go/url-shortener
go mod init github.com/yourusername/url-shortener
go mod tidy
go run cmd/server/main.go

# Blog API
cd go/blog-api
go mod init github.com/yourusername/blog-api
go mod tidy
go run cmd/server/main.go
```

### Python Projects

```bash
# Weather CLI
cd python/weather-cli
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python -m weather_cli current "Bangkok"

# Web Scraper
cd python/web-scraper
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m web_scraper --config example_config.yaml
```

## Learning Resources

### Documentation
- [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) - Step-by-step conversion guide
- [APPLICATION_SELECTION.md](APPLICATION_SELECTION.md) - Choose the right app
- [COPILOT_GUIDE.md](COPILOT_GUIDE.md) - Copilot tips & techniques
- [WORKSHOP_PROGRESS.md](WORKSHOP_PROGRESS.md) - Track your progress

### External Resources
- [Go Documentation](https://go.dev/doc/)
- [Python Documentation](https://docs.python.org/3/)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)

## Common Conversions

### Go → Python
| Go Pattern | Python Equivalent |
|------------|-------------------|
| `struct` | `dataclass` or `Pydantic model` |
| `interface` | `Protocol` or `ABC` |
| `error returns` | `exceptions` |
| `goroutines` | `asyncio tasks` |
| `defer` | `context managers` |
| `Chi/Gin` | `FastAPI/Django` |

### Python → Go
| Python Pattern | Go Equivalent |
|----------------|---------------|
| `class` | `struct` with methods |
| `async/await` | `goroutines` |
| `exceptions` | `error returns` |
| `decorators` | function wrappers |
| `context managers` | `defer` |
| `Click/argparse` | `Cobra` |

## Tips for Success

1. ✅ **Read First** - เข้าใจโค้ดต้นฉบับก่อนแปลง
2. ✅ **Go Slow** - Convert ทีละ module
3. ✅ **Test Often** - Run tests หลังแปลงแต่ละส่วน
4. ✅ **Use Copilot** - แต่อ่านและเข้าใจก่อน accept
5. ✅ **Ask Questions** - ใช้ Copilot Chat เมื่อติดปัญหา
6. ✅ **Stay Idiomatic** - เขียนโค้ดที่เป็นธรรมชาติในภาษาปลายทาง
7. ✅ **Document** - อธิบายการเปลี่ยนแปลงที่สำคัญ
8. ✅ **Track Progress** - อัพเดท WORKSHOP_PROGRESS.md

## Troubleshooting

### Copilot Not Working?
- Check Copilot status in VS Code status bar
- Restart VS Code
- Check your GitHub Copilot subscription
- Try `Cmd+Shift+P` → "Reload Window"

### Conversion Stuck?
- Review [COPILOT_GUIDE.md](COPILOT_GUIDE.md) for techniques
- Use Copilot Chat to ask for help
- Check [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for detailed steps
- Ask the instructor

### Tests Failing?
- Compare with original behavior
- Check error messages carefully
- Use `/fix` in Copilot Chat
- Review conversion of error handling

## Contributing

Found an issue or have a suggestion?
1. Check existing issues
2. Create a new issue with details
3. Submit a pull request (if applicable)

## License

This workshop material is provided for educational purposes.

## Credits

Created for GitHub Copilot Workshop - Convert Framework  
Demonstrating cross-language code conversion with AI assistance

---

## Next Steps

1. 📖 Read [APPLICATION_SELECTION.md](APPLICATION_SELECTION.md) to choose your app
2. 📝 Review [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for detailed steps
3. 🤖 Study [COPILOT_GUIDE.md](COPILOT_GUIDE.md) for techniques
4. 🚀 Start converting!
5. ✅ Track progress in [WORKSHOP_PROGRESS.md](WORKSHOP_PROGRESS.md)

**Happy Converting! 🎉**
