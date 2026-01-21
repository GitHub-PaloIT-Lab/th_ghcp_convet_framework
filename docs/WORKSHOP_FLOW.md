# Workshop Flow - 30 นาที Demo การแปลง Go → Python

## ภาพรวม Workshop

**ระยะเวลา**: 30 นาที  
**รูปแบบ**: Instructor demo แบบ live coding  
**เป้าหมาย**: แสดงวิธีใช้ GitHub Copilot ในการแปลง Go models เป็น Python Pydantic models  
**ผู้เข้าร่วม**: ดู demo จาก repository นี้

---

## โครงสร้าง Workshop

### 1. Introduction & Code Review (5 นาที)

**วัตถุประสงค์**: ให้ผู้เข้าร่วมเข้าใจโครงสร้างและโค้ด Go ที่จะแปลง

**สิ่งที่ต้องทำ**:

1. **เปิดไฟล์ Go source code**
   - เปิด [go/url-shortener/internal/models/url.go](../go/url-shortener/internal/models/url.go)
   - อธิบายโครงสร้าง URL Shortener application

2. **อธิบาย Go structs**
   ```go
   type URL struct {
       ID          int64     `json:"id"`
       ShortCode   string    `json:"short_code"`
       OriginalURL string    `json:"original_url"`
       UserID      string    `json:"user_id"`
       CreatedAt   time.Time `json:"created_at"`
   }
   
   type Click struct {
       ID         int64     `json:"id"`
       ShortCode  string    `json:"short_code"`
       ClickedAt  time.Time `json:"clicked_at"`
       Referrer   string    `json:"referrer,omitempty"`
   }
   ```

3. **ใช้ Copilot Chat `/explain` command**
   - เลือกโค้ด Go struct
   - พิมพ์: `/explain`
   - ให้ Copilot อธิบาย Go patterns:
     - Struct tags (`json:"..."`)
     - Pointer types
     - time.Time type
     - `omitempty` tag

4. **Highlight จุดสำคัญที่ต้องแปลง**:
   - `int64` → `int` (Python)
   - `time.Time` → `datetime`
   - `omitempty` → `Optional[str]`
   - PascalCase → snake_case
   - Struct tags → Pydantic Field aliases

---

### 2. Live Conversion Demo - Basic Models (7 นาที)

**วัตถุประสงค์**: แปลง Go structs เป็น Python Pydantic models

**ขั้นตอน**:

1. **สร้างไฟล์ Python ใหม่**
   - สร้างไฟล์: `python/url-shortener-py/models/url.py`

2. **Prompt 1: การแปลงพื้นฐาน**

   **พิมพ์ Prompt ใน Copilot Chat**:
   ```
   Convert the Go models from go/url-shortener/internal/models/url.go to Python Pydantic models.
   Create python/url-shortener-py/models/url.py with the following:

   - Convert URL, Click, CreateURLRequest, and CreateURLResponse structs to Pydantic BaseModel classes
   - Map Go types to Python types: int64 → int, time.Time → datetime, string → str
   - Convert PascalCase field names to snake_case
   - Keep JSON field names matching the Go struct tags using Field(alias="...")
   - Make referrer field Optional[str] = None since it has omitempty in Go
   - Add proper imports: from pydantic import BaseModel, Field; from datetime import datetime
   - Add docstrings explaining each model's purpose
   ```

3. **แสดงการรับ Suggestions**
   - Copilot จะ generate code
   - แสดงวิธี accept/reject suggestions
   - อธิบายว่าทำไม Copilot ถึงแปลงแบบนี้

4. **ผลลัพธ์ที่คาดหวัง**:
   ```python
   from pydantic import BaseModel, Field
   from datetime import datetime
   from typing import Optional

   class URL(BaseModel):
       """URL model representing shortened URLs in the database.
       Converted from Go url-shortener models."""
       
       id: int = Field(alias="id")
       short_code: str = Field(alias="short_code")
       original_url: str = Field(alias="original_url")
       user_id: str = Field(alias="user_id")
       created_at: datetime = Field(alias="created_at")

   class Click(BaseModel):
       """Click tracking model for analytics.
       referrer field is optional (omitempty in Go)."""
       
       id: int = Field(alias="id")
       short_code: str = Field(alias="short_code")
       clicked_at: datetime = Field(alias="clicked_at")
       referrer: Optional[str] = Field(default=None, alias="referrer")
   ```

5. **Tips สำหรับผู้เข้าร่วม**:
   - เขียน comments เป็นไทยก่อน Copilot จะช่วยได้ดีขึ้น
   - ตรวจสอบ type mapping ให้ถูกต้อง
   - ใช้ Field(alias="...") เพื่อรักษา JSON field names

---

### 3. Add Validation Rules (7 นาที)

**วัตถุประสงค์**: เพิ่ม validation ที่เป็น Python/Pydantic specific

**ขั้นตอน**:

1. **Prompt 2: เพิ่ม Validators**

   **พิมพ์ Prompt ใน Copilot Chat**:
   ```
   Add Pydantic validators to the URL and Click models in python/url-shortener-py/models/url.py:

   For URL model:
   - short_code: must be 6-10 characters, alphanumeric only
   - original_url: must be a valid HTTP/HTTPS URL using HttpUrl type
   - user_id: cannot be empty string

   For CreateURLRequest:
   - original_url: must be valid HTTP/HTTPS URL, max length 2048 characters

   Use Pydantic v2 syntax with field_validator decorator and Field constraints.
   Add helpful error messages for each validation.
   ```

2. **แสดงการเพิ่ม Validators**
   - Copilot จะแนะนำ `@field_validator` decorators
   - แสดงวิธีใช้ `HttpUrl` type
   - เพิ่ม `Field(min_length=..., max_length=..., pattern=...)`

3. **ผลลัพธ์ที่คาดหวัง**:
   ```python
   from pydantic import BaseModel, Field, field_validator, HttpUrl
   from datetime import datetime
   from typing import Optional
   import re

   class URL(BaseModel):
       """URL model with validation rules."""
       
       id: int = Field(alias="id")
       short_code: str = Field(
           min_length=6,
           max_length=10,
           pattern=r'^[a-zA-Z0-9]+$',
           alias="short_code"
       )
       original_url: HttpUrl = Field(alias="original_url")
       user_id: str = Field(min_length=1, alias="user_id")
       created_at: datetime = Field(alias="created_at")

       @field_validator('short_code')
       @classmethod
       def validate_short_code(cls, v: str) -> str:
           if not re.match(r'^[a-zA-Z0-9]+$', v):
               raise ValueError('Short code must be alphanumeric only')
           return v
   ```

4. **ทดสอบ Validation**
   - สร้าง instance ที่ invalid
   - แสดง error messages
   ```python
   # ทดสอบใน Python REPL
   try:
       url = URL(
           id=1,
           short_code="abc",  # สั้นเกินไป!
           original_url="https://example.com",
           user_id="user123",
           created_at=datetime.now()
       )
   except ValidationError as e:
       print(e)  # แสดง error message ที่ชัดเจน
   ```

---

### 4. Generate Tests (7 นาті)

**วัตถุประสงค์**: ใช้ Copilot สร้าง pytest tests อัตโนมัติ

**ขั้นตอน**:

1. **สร้างไฟล์ test ใหม่**
   - สร้าง: `python/url-shortener-py/tests/test_models.py`

2. **Prompt 3: Generate Tests**

   **พิมพ์ Prompt ใน Copilot Chat**:
   ```
   Create comprehensive pytest tests for the Pydantic models in python/url-shortener-py/tests/test_models.py:

   For URL model test:
   - Test valid URL creation with all fields
   - Test JSON serialization preserves Go field names (id, short_code, etc.)
   - Test datetime handling for created_at field
   - Test short_code validation (length and alphanumeric)

   For Click model test:
   - Test with and without referrer field
   - Test omitempty behavior (referrer not included in JSON when None)

   For CreateURLRequest test:
   - Test URL validation (valid HTTP/HTTPS)
   - Test invalid URLs raise ValidationError
   - Test max length constraint

   Use pytest fixtures for sample data. Import necessary types from pydantic.
   ```

3. **แสดง Test Generation**
   - Copilot สร้าง fixtures
   - สร้าง test cases ทั้ง positive และ negative
   - แสดง assertion patterns

4. **ผลลัพธ์ที่คาดหวัง**:
   ```python
   import pytest
   from datetime import datetime
   from pydantic import ValidationError
   from models.url import URL, Click, CreateURLRequest

   @pytest.fixture
   def sample_url_data():
       return {
           "id": 1,
           "short_code": "abc123",
           "original_url": "https://example.com",
           "user_id": "user123",
           "created_at": datetime.now()
       }

   def test_url_creation(sample_url_data):
       """Test creating a valid URL model"""
       url = URL(**sample_url_data)
       assert url.short_code == "abc123"
       assert str(url.original_url) == "https://example.com/"

   def test_url_json_serialization(sample_url_data):
       """Test JSON serialization preserves Go field names"""
       url = URL(**sample_url_data)
       json_data = url.model_dump(by_alias=True)
       assert "short_code" in json_data
       assert "shortCode" not in json_data

   def test_short_code_too_short():
       """Test short_code validation fails for short codes"""
       with pytest.raises(ValidationError) as exc_info:
           URL(
               id=1,
               short_code="abc",  # Too short!
               original_url="https://example.com",
               user_id="user123",
               created_at=datetime.now()
           )
       assert "short_code" in str(exc_info.value)
   ```

5. **รัน Tests**
   ```bash
   pytest tests/test_models.py -v
   ```

6. **แสดงผลลัพธ์**
   - Tests pass แสดงว่าการแปลงถูกต้อง
   - อธิบายความสำคัญของ tests ในการ validate conversion

---

### 5. Wrap-up & Resources (4 นาที)

**วัตถุประสงค์**: สรุปและให้ resources สำหรับการเรียนรู้ต่อ

**สิ่งที่ต้องทำ**:

1. **แสดงไฟล์ที่แปลงเสร็จแล้ว**
   - เปิด `url.py` และ `test_models.py` ข้างกัน
   - เปรียบเทียบกับ Go original
   - แสดงความแตกต่างและความคล้ายกัน

2. **สรุป Conversion Patterns**
   - ✅ **Type Mapping**: `int64` → `int`, `time.Time` → `datetime`
   - ✅ **Naming**: PascalCase → snake_case
   - ✅ **Validation**: Struct tags → Pydantic validators
   - ✅ **Optional Fields**: `omitempty` → `Optional[T]`
   - ✅ **Error Handling**: Go errors → Python exceptions
   - ✅ **Testing**: Table-driven tests → pytest parametrize

3. **Copilot Features ที่ใช้**
   - `/explain` - อธิบายโค้ด
   - `/tests` - สร้าง tests
   - `/doc` - สร้าง documentation
   - Chat prompts - แปลงโค้ดและเพิ่ม features
   - Inline suggestions - เติมโค้ดอัตโนมัติ

4. **Resources สำหรับการเรียนรู้ต่อ**
   - 📖 [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) - แปลง modules อื่นๆ
   - 🤖 [COPILOT_GUIDE.md](COPILOT_GUIDE.md) - Prompts และ techniques เพิ่มเติม
   - 📝 [APPLICATION_SELECTION.md](APPLICATION_SELECTION.md) - เลือก app อื่นๆ
   - 📚 [.github/copilot-instructions.md](../.github/copilot-instructions.md) - Best practices

5. **Next Steps สำหรับผู้เข้าร่วม**:
   - ✅ ลองแปลง Analytics model ต่อ
   - ✅ แปลง Service layer (business logic)
   - ✅ แปลง Storage layer (cache, database)
   - ✅ แปลง API handlers (FastAPI routes)
   - ✅ เพิ่ม integration tests
   - ✅ Deploy application

6. **Q&A (3 นาที)**
   - เปิดรับคำถาม
   - ตอบข้อสงสัย
   - แชร์ tips เพิ่มเติม

---

## Copilot Prompts - Quick Reference

### 🔄 Conversion Prompts

```
Convert [source file] from Go to Python Pydantic models
- Map types: int64→int, time.Time→datetime, string→str
- Convert naming: PascalCase→snake_case
- Preserve JSON tags as Field(alias="...")
- Handle omitempty as Optional types
```

### ✅ Validation Prompts

```
Add Pydantic validators for [model name]:
- Field constraints (min/max length, pattern)
- Type validation (HttpUrl, EmailStr)
- Custom validators with @field_validator
- Error messages in Thai/English
```

### 🧪 Test Generation Prompts

```
Generate pytest tests for [model/function]:
- Fixtures for sample data
- Positive test cases
- Negative test cases (ValidationError)
- Edge cases
- JSON serialization tests
```

### 📝 Documentation Prompts

```
Add comprehensive docstrings to [file]:
- Google-style docstrings
- Attributes section
- Examples section
- Notes about Go conversion
```

---

## Tips สำหรับ Instructor

### ⏰ Time Management

- **5 นาที** - Intro (อย่าเกิน!)
- **7 นาที** - Basic conversion (focus ที่ใจความสำคัญ)
- **7 นาที** - Validation (แสดง error handling)
- **7 นาที** - Tests (รัน tests ให้เห็น)
- **4 นาที** - Wrap-up (เหลือเวลา Q&A)

### 💡 Engagement Tips

1. **แสดง Mistakes**
   - ทำผิดบ้างเพื่อแสดงวิธีแก้
   - ให้ Copilot ช่วย debug
   - เรียนรู้จาก errors

2. **ถามคำถาม**
   - "ทำไมต้องใช้ Optional ที่นี่?"
   - "Pydantic ดีกว่า dataclass ตรงไหน?"
   - "จะทดสอบ validation นี้ยังไง?"

3. **แชร์ Insights**
   - "Trick นี้ทำให้ Copilot แนะนำดีขึ้น"
   - "Pattern นี้ใช้บ่อยใน production"
   - "ข้อควรระวังตรงนี้"

### 🎯 Learning Objectives

ให้แน่ใจว่าผู้เข้าร่วมเข้าใจ:

- ✅ วิธีใช้ Copilot Chat และ inline suggestions
- ✅ Type mapping ระหว่าง Go และ Python
- ✅ Pydantic models และ validation
- ✅ การสร้าง tests ด้วย Copilot
- ✅ Best practices ในการแปลงโค้ด
- ✅ ทำไม Python/Pydantic เหมาะกับ use cases นี้

### 🔧 Troubleshooting

**ถ้า Copilot ไม่ทำงาน**:
- ตรวจสอบ status bar (เขียว = OK)
- Reload VS Code
- ใช้ Chat แทน inline suggestions

**ถ้าเวลาไม่พอ**:
- Skip validation section
- แสดงแค่ basic conversion + tests
- อ้างอิง guide สำหรับ advanced topics

**ถ้าเหลือเวลา**:
- แปลง Analytics model ต่อ
- แสดง async/await patterns
- ทำ integration test

---

## File Structure After Demo

```
python/url-shortener-py/
├── models/
│   └── url.py                 # ✅ Converted models with validation
├── tests/
│   └── test_models.py         # ✅ Comprehensive pytest tests
├── requirements.txt           # pydantic, pytest
└── README.md                  # Setup instructions
```

---

## Expected Outcomes

ผู้เข้าร่วมจะได้เรียนรู้:

1. **Technical Skills**
   - ✅ การแปลง Go structs → Python Pydantic models
   - ✅ Type mapping และ naming conventions
   - ✅ Validation ด้วย Pydantic
   - ✅ Testing ด้วย pytest

2. **Copilot Skills**
   - ✅ การใช้ Chat prompts อย่างมีประสิทธิภาพ
   - ✅ Slash commands (/explain, /tests, /doc)
   - ✅ Inline suggestions best practices
   - ✅ การ review และ accept/reject suggestions

3. **Practical Knowledge**
   - ✅ เมื่อไหร่ควรแปลง Go → Python
   - ✅ Trade-offs ของแต่ละภาษา
   - ✅ Best practices ในการแปลงโค้ด
   - ✅ วิธีต่อยอดเป็น full application

---

## Post-Workshop

### สำหรับผู้เข้าร่วม

**ลองทำต่อ**:
1. แปลง Analytics model
2. แปลง Service layer
3. สร้าง FastAPI endpoints
4. เพิ่ม Redis caching
5. Deploy แบบ production

**เรียนรู้เพิ่ม**:
- Pydantic documentation
- FastAPI tutorial
- pytest best practices
- Docker containerization

### สำหรับ Instructor

**Collect Feedback**:
- อะไรที่ชัดเจน/ไม่ชัดเจน
- Pace เหมาะสมไหม
- Topics ที่อยากเห็นเพิ่ม
- Copilot ช่วยได้มากแค่ไหน

**Improve Workshop**:
- Update prompts ที่ได้ผลดีขึ้น
- เพิ่ม examples ที่ชัดเจนกว่า
- ปรับ timing ตามความเหมาะสม
- เพิ่ม troubleshooting tips

---

## Success Metrics

Workshop ประสบความสำเร็จเมื่อ:

- ✅ ผู้เข้าร่วมเข้าใจ conversion patterns
- ✅ สามารถใช้ Copilot prompts ได้
- ✅ เห็น value ของ Pydantic validation
- ✅ รู้วิธีสร้าง tests อัตโนมัติ
- ✅ มีความมั่นใจแปลงโค้ดเอง
- ✅ มี portfolio piece ที่เป็นประโยชน์

---

**Happy Coding with GitHub Copilot! 🚀**
