# Advanced Image Compressor Pro

## English

### Overview
**Advanced Image Compressor Pro** is a cutting-edge, cross-platform desktop application built with Python, PyQt6, and Pillow. It offers professional-grade image compression using multiple advanced algorithms, including JPEG, PNG, WebP, DCT Quantization, Wavelet, Fractal, Hybrid, and Custom combinations. With real-time previews, detailed statistics, and a modern UI inspired by Windows 11, it supports lossless and lossy compression for optimal file size reduction without sacrificing quality.

### Key Features
- **Multiple Compression Methods**: JPEG (lossy), PNG (lossless optimization), WebP, DCT-based Quantization, Wavelet Transform, Experimental Fractal, Hybrid (JPEG + Wavelet), and fully Custom pipelines.
- **Advanced Controls**: Quality sliders, compression levels, pre-filters (Blur, Sharpen, Contrast), dithering, palette reduction (up to 256 colors), and algorithm selection (Deflate, LZMA, BZip2).
- **Real-Time Preview**: Side-by-side original vs. compressed views with scalable pixmaps.
- **Statistics Dashboard**: Original size, compressed size (KB), and compression ratio (%) displayed instantly.
- **Multi-Language Support**: English, فارسی (Persian with RTL), 中文 (Chinese), Русский (Russian) – fully translated UI with dynamic layout direction.
- **Theme Customization**: Windows 11, Dark, Light, Windows Default, Red, and Blue themes with gradient backgrounds and modern styling.
- **Threaded Compression**: Non-blocking UI with progress bar and detailed logging.
- **System Tray Integration**: Minimize to tray with restore/quit options and notification on minimize.
- **Export & Metadata**: Save in JPEG, PNG, or WebP; preserves compression log.
- **Keyboard & Menu Shortcuts**: Intuitive file operations and help dialogs.

### Requirements
- Python 3.8+
- PyQt6
- Pillow (PIL)
- numpy
- scipy
- pywt (PyWavelets)
- opencv-python (cv2)
- qdarkstyle
- qtawesome

### Installation
1. Ensure Python is installed.
2. Install dependencies:
   ```bash
   pip install PyQt6 Pillow numpy scipy pywavelets opencv-python qdarkstyle qtawesome
   ```
3. Run the application:
   ```bash
   python image_compressor.py
   ```

### Usage
- **Interface Setup**: Choose language and theme from dropdowns.
- **Select Method**: Pick from 8 advanced compression techniques via radio buttons.
- **Tune Settings**: Adjust quality, level, filters, and more in the tabbed panel.
- **Load Image**: Open PNG, JPG, JPEG, BMP, WebP, or GIF files.
- **Compress**: Click "Compress" – watch progress and view results instantly.
- **Analyze**: Check stats and preview compressed image.
- **Save**: Export the optimized file.

### Screenshots
- Modern dual-panel layout with controls and previews  
- Custom combination tab for building compression pipelines  
- Windows 11 theme with smooth gradients and rounded elements  
- RTL support in Persian mode with full translation  
- System tray minimization with context menu  

### Technical Highlights
- **DCT Quantization**: Custom 8x8 block processing with adjustable quantization table.
- **Wavelet Compression**: Daubechies wavelet (db1) with soft thresholding.
- **Fractal Approximation**: Experimental resizing-based iterated function system.
- **Hybrid & Custom**: Chain multiple algorithms for ultimate control.
- **Pre-Processing**: Gaussian blur, sharpening, contrast enhancement.
- **Palette Optimization**: Adaptive palette with Floyd-Steinberg dithering.

### Contributing
Fork the repository, enhance algorithms, or add new methods. Pull requests and issues are welcome!

### License
MIT License – Free for personal and commercial use, modification, and distribution.

---

## فارسی

### بررسی اجمالی
**فشرده‌ساز پیشرفته تصویر پرو** یک برنامه دسکتاپ حرفه‌ای و چندپلتفرمی است که با پایتون، PyQt6 و Pillow ساخته شده. این ابزار فشرده‌سازی پیشرفته تصاویر را با الگوریتم‌های متنوع مانندured: JPEG، PNG، WebP، کوانتیزاسیون DCT، موجکی، فراکتال، ترکیبی و ترکیب سفارشی ارائه می‌دهد. با پیش‌نمایش لحظه‌ای، آمار دقیق و رابط کاربری مدرن الهام‌گرفته از ویندوز ۱۱، فشرده‌سازی بدون اتلاف و با اتلاف را برای کاهش بهینه حجم فایل بدون افت کیفیت پشتیبانی می‌کند.

### ویژگی‌های کلیدی
- **روش‌های فشرده‌سازی متعدد**: JPEG (با اتلاف)، PNG (بهینه‌سازی بدون اتلاف)، WebP، کوانتیزاسیون مبتنی بر DCT، تبدیل موجکی، فراکتال آزمایشی، ترکیبی (JPEG + موجکی) و pipeline سفارشی.
- **کنترل‌های پیشرفته**: اسلایدر کیفیت، سطوح فشرده‌سازی، پیش‌فیلترها (بلور، تیز کردن، کنتراست)، دیترینگ، کاهش پالت (تا ۲۵۶ رنگ) و انتخاب الگوریتم (Deflate، LZMA، BZip2).
- **پیش‌نمایش لحظه‌ای**: نمایش کنار هم تصویر اصلی و فشرده با مقیاس‌پذیری نرم.
- **داشبورد آمار**: حجم اصلی، حجم فشرده (کیلوبایت) و نسبت فشرده‌سازی (%) به‌صورت آنی.
- **پشتیبانی چندزبانه**: انگلیسی، فارسی (با راست‌چین)، چینی، روسی – ترجمه کامل UI با جهت چیدمان پویا.
- **تم‌های سفارشی**: ویندوز ۱۱، تاریک، روشن، پیش‌فرض ویندوز، قرمز و آبی با پس‌زمینه‌های گرادیانتی.
- **فشرده‌سازی تردشده**: بدون بلاک UI با نوار پیشرفت و لاگ دقیق.
- **ادغام با سینی سیستم**: مینیمایز به tray با گزینه‌های بازگردانی/خروج و نوتیفیکیشن.
- **خروجی و متادیتا**: ذخیره در JPEG، PNG یا WebP؛ حفظ لاگ فشرده‌سازی.
- **میانبرهای کیبورد و منو**: عملیات فایل intuitiv و دیالوگ‌های راهنما.

### پیش‌نیازها
- پایتون ۳.۸ یا بالاتر
- PyQt6
- Pillow (PIL)
- numpy
- scipy
- pywavelets
- opencv-python (cv2)
- qdarkstyle
- qtawesome

### نصب
۱. پایتون را نصب کنید.
۲. وابستگی‌ها را نصب نمایید:
   ```bash
   pip install PyQt6 Pillow numpy scipy pywavelets opencv-python qdarkstyle qtawesome
   ```
۳. برنامه را اجرا کنید:
   ```bash
   python image_compressor.py
   ```

### نحوه استفاده
- **تنظیم رابط**: زبان و تم را از منوهای کشویی انتخاب کنید.
- **انتخاب روش**: یکی از ۸ تکنیک پیشرفته را با دکمه‌های رادیویی برگزینید.
- **تنظیم پارامترها**: کیفیت، سطح، فیلترها و غیره را در پنل تب‌دار تنظیم کنید.
- **بارگزاری تصویر**: فایل‌های PNG، JPG، JPEG، BMP، WebP یا GIF را باز کنید.
- **فشرده‌سازی**: روی "فشرده‌سازی" کلیک کنید – پیشرفت را ببینید و نتیجه را فوراً مشاهده کنید.
- **تحلیل**: آمار و پیش‌نمایش تصویر فشرده را بررسی کنید.
- **ذخیره**: فایل بهینه‌شده را صادر کنید.

### تصاویر
- چیدمان دوپنل مدرن با کنترل‌ها و پیش‌نمایش‌ها  
- تب ترکیب سفارشی برای ساخت pipeline فشرده‌سازی  
- تم ویندوز ۱۱ با گرادیانت‌های نرم و عناصر گرد  
- پشتیبانی راست‌چین در حالت فارسی با ترجمه کامل  
- مینیمایز به سینی سیستم با منوی زمینه  

### نکات فنی
- **کوانتیزاسیون DCT**: پردازش بلوک ۸x۸ سفارشی با جدول کوانتیزاسیون قابل تنظیم.
- **فشرده‌سازی موجکی**: موجک Daubechies (db1) با آستانه‌گذاری نرم.
- **تقریب فراکتال**: روش آزمایشی مبتنی بر تغییر اندازه.
- **ترکیبی و سفارشی**: زنجیره‌سازی چندین الگوریتم برای کنترل کامل.
- **پیش‌پردازش**: بلور گاوسی، تیز کردن، افزایش کنتراست.
- **بهینه‌سازی پالت**: پالت تطبیقی با دیترینگ Floyd-Steinberg.

### مشارکت
ریپازیتوری را فورک کنید، الگوریتم‌ها را بهبود بخشید یا روش‌های جدید اضافه کنید. Pull requestها و مسائل خوش‌آمد!

### مجوز
مجوز MIT – آزاد برای استفاده شخصی و تجاری، تغییر و توزیع.

---

## 中文

### 概述
**高级图像压缩专业版** 是一款前沿的跨平台桌面应用程序，使用 Python、PyQt6 和 Pillow 构建。它提供专业级图像压缩，支持多种高级算法，包括 JPEG、PNG、WebP、DCT 量化、小波、实验性分形、混合（JPEG + 小波）以及自定义组合。具备实时预览、详细统计和 Windows 11 风格现代 UI，支持有损和无损压缩，在不牺牲质量的前提下实现最佳文件大小缩减。

### 主要功能
- **多种压缩方法**：JPEG（有损）、PNG（无损优化）、WebP、DCT 量化、小波变换、实验性分形、混合（JPEG + 小波）以及完全自定义管道。
- **高级控制**：质量滑块、压缩级别、预过滤（模糊、锐化、对比度）、抖动、调色板缩减（最多 256 色）以及算法选择（Deflate、LZMA、BZip2）。
- **实时预览**：原图与压缩图并排显示，支持平滑缩放。
- **统计仪表板**：即时显示原始大小、压缩大小（KB）和压缩比率（%）。
- **多语言支持**：英语、波斯语（RTL）、中文、俄语 – 完整 UI 翻译，动态布局方向。
- **主题自定义**：Windows 11、暗黑、亮模式、Windows 默认、红色和蓝色主题，带渐变背景。
- **线程压缩**：非阻塞 UI，带进度条和详细日志。
- **系统托盘集成**：最小化到托盘，支持恢复/退出选项及最小化通知。
- **导出与元数据**：保存为 JPEG、PNG 或 WebP；保留压缩日志。
- **键盘与菜单快捷键**：直观文件操作和帮助对话框。

### 要求
- Python 3.8+
- PyQt6
- Pillow (PIL)
- numpy
- scipy
- pywavelets
- opencv-python (cv2)
- qdarkstyle
- qtawesome

### 安装
1. 确保已安装 Python。
2. 安装依赖项：
   ```bash
   pip install PyQt6 Pillow numpy scipy pywave/esm qdarkstyle qtawesome
   ```
3. 运行应用程序：
   ```bash
   python image_compressor.py
   ```

### 使用方法
- **界面设置**：从下拉菜单选择语言和主题。
- **选择方法**：通过单选按钮挑选 8 种高级压缩技术。
- **调整设置**：在选项卡面板中微调质量、级别、过滤器等。
- **加载图像**：打开 PNG、JPG、JPEG、BMP、WebP 或 GIF 文件。
- **压缩**：点击“压缩图像” – 观察进度并即时查看结果。
- **分析**：检查统计数据和压缩图像预览。
- **保存**：导出优化后的文件。

### 截图
- 现代双面板布局，带控制和预览  
- 自定义组合选项卡，用于构建压缩管道  
- Windows 11 主题，平滑渐变和圆角元素  
- 波斯语模式下的 RTL 支持及完整翻译  
- 系统托盘最小化，带上下文菜单  

### 技术亮点
- **DCT 量化**：自定义 8x8 块处理，可调量化表。
- **小波压缩**：Daubechies 小波 (db1) 带软阈值。
- **分形逼近**：基于调整大小的迭代函数系统实验方法。
- **混合与自定义**：链式多个算法，实现终极控制。
- **预处理**：高斯模糊、锐化、对比度增强。
- **调色板优化**：自适应调色板，Floyd-Steinberg 抖动。

### 贡献
Fork 仓库，优化算法或添加新方法。欢迎 Pull Request 和问题反馈！

### 许可证
MIT 许可证 – 免费用于个人和商业目的、修改和分发。