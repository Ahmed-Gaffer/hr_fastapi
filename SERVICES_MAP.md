# Services map — خريطة الخدمات في app/services

- import_excel.py
  - وظيفة: تحويل ملفات Excel/CSV إلى سجلات قابلة للحفظ (mapping headers, تنظيف القيم).
  - مستدعى من: app/routes/imports.py (أو عبر adapter الجديد).
  - ملاحظات: يعتمد على صيغ أوراق محددة ويجب أن يتوافق مع ملف التجهيز الشامل.

- smart_importer.py
  - وظيفة: SmartSalaryImporter — استيراد متقدّم مع قواعد توفيق وتحويل بيانات معقّدة.
  - مستدعى من: bulk_importer_v3.py أو يمكن استدعاؤه مباشرة عبر adapter.
  - ملاحظات: قوي في التعامل مع حالات غير متوقعة، لكن واجهته مختلفة.

- bulk_importer_v3.py
  - وظيفة: BulkImporter (v3) — معالجة دفعات واستيراد متكامل (قد يحتوي على import_file/import_from_stream).
  - مستدعى من: سابقاً من راوترات مباشرة، الآن عبر adapter.
  - ملاحظات: قد يكون هو "مصدر الحقيقة" للعمليات الكبرى.

- professional_salary_calculator.py
  - وظيفة: محسب رواتب احترافي (خوارزميات حسابية مفصّلة).
  - مستدعى من: endpoints حساب الرواتب / تقارير.
  - ملاحظات: تستخدمه الراوترات لحساب سجل معين.

- comprehensive_salary_calculator.py, advanced_salary_calculator.py, salary_calculator.py, salary_logic.py
  - وظيفة: محاسبات رواتب بديلة/مساعدة.
  - مستدعى من: services أو اختبارات.
  - ملاحظات: يوجد تكرار وظيفي — يجب توحيد واجهة حساب مستقبلًا.

- benefit_calculator.py, insurance_calculator.py, tax_engine.py
  - وظيفة: حساب مكونات منفصلة للراتب.
  - مستدعى من: calculators أو importers.

- auth.py
  - وظيفة: منطق المصادقة وإصدار التوكن.
  - مستدعى من: routes/auth.py و dependencies.

- ملفات مرشحة للمراجعة/حذف لاحقًا
  - app/api/imports.py  ← محتمل تكرار (راجع قبل حذف).
  - Untitled-* في services/routes ← مسودات، لا تُحذف الآن.

# توصية تنظيمية قصيرة
1. الاحتفاظ بملفات models كما هي.
2. استخدام adapter (هذا الملف) كواجهة وحيدة لكل راوترات الاستيراد.
3. بعد اختبار ناجح، وسمّ الملفات القديمة بـdeprecate ثم حذف تدريجي.