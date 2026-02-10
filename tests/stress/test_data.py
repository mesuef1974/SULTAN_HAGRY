"""
بيانات تجريبية لاختبارات التحمل
Test Data for Stress Testing
"""

# بيانات المستخدمين للاختبار
TEST_USERS = [
    {
        "username": "test_user",
        "password": "test_password",
        "role": "teacher"
    },
    {
        "username": "test_admin",
        "password": "test_password",
        "role": "admin"
    },
    {
        "username": "test_viewer",
        "password": "test_password",
        "role": "viewer"
    }
]

# نماذج من بنود الخطة التشغيلية للاختبار
SAMPLE_PLAN_ITEMS = [
    "تطوير المناهج",
    "تحسين البنية التحتية",
    "برامج التطوير المهني",
    "الأنشطة الطلابية",
    "التقييم والجودة"
]

# نماذج من اللجان
SAMPLE_COMMITTEES = [
    "لجنة الجودة",
    "لجنة الأنشطة",
    "لجنة التطوير المهني",
    "لجنة الامتحانات"
]

# معلومات إضافية للاختبار
TEST_CONFIG = {
    "max_users": 50,
    "spawn_rate": 10,
    "test_duration": 600,  # 10 minutes
    "target_response_time": 2000,  # 2 seconds
    "max_failure_rate": 0.01  # 1%
}
