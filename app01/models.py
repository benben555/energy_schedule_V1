from django.db import models


class Consumers(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=16)
    phone = models.CharField(verbose_name="手机号", max_length=16)
    remain_power = models.DecimalField(verbose_name="剩余电量", max_digits=10, decimal_places=2, default=0)
    a1 = models.BinaryField(verbose_name="SK_A1", max_length=1024)
    a2 = models.BinaryField(verbose_name="SK_A2", max_length=1024)
    b1 = models.BinaryField(verbose_name="PK_A1(bytes)", max_length=1024)
    sb1 = models.CharField(verbose_name="PK_A1(string)", max_length=1024)
    b2 = models.BinaryField(verbose_name="PK_A2(bytes)", max_length=1024)
    sb2 = models.CharField(verbose_name="PK_A2(string)", max_length=1024)
    priority = models.DecimalField(verbose_name="优先级", max_digits=10, decimal_places=2)
    status = models.CharField(verbose_name="当前状态", default="未参与本轮调度", max_length=128)


class Trapdoor(models.Model):
    index = models.IntegerField(verbose_name="调度轮数", default=0)
    keyword = models.CharField(verbose_name="关键字", max_length=16)
    # lambda1 = models.CharField(verbose_name="lambda1", max_length=1024)
    # lambda2 = models.CharField(verbose_name="lambda2", max_length=1024)
    st = models.BinaryField(verbose_name="陷门", max_length=1024)
    trapdoor_time = models.DateTimeField(verbose_name="调度时间", auto_now_add=True)
    userid = models.ForeignKey(to="Consumers", to_field="id", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['index', 'userid'], name='uc_index_userid')
        ]


class Gsp(models.Model):
    p = models.BinaryField(verbose_name="生成元", max_length=1024)
    sk_s = models.BinaryField(verbose_name="服务器私钥", max_length=1024)
    pk_s = models.BinaryField(verbose_name="服务器公钥(bytes)", max_length=1024)
    spk_s = models.CharField(verbose_name="服务器公钥(string)", max_length=1024)
    sk_B1 = models.BinaryField(verbose_name="MGCC私钥1", max_length=1024)
    pk_B1 = models.BinaryField(verbose_name="MGCC公钥1(bytes)", max_length=1024)
    spk_B1 = models.CharField(verbose_name="MGCC公钥1(string)", max_length=1024)
    sk_B2 = models.BinaryField(verbose_name="MGCC私钥2", max_length=1024)
    pk_B2 = models.BinaryField(verbose_name="MGCC公钥2(bytes)", max_length=1024)
    spk_B2 = models.CharField(verbose_name="MGCC公钥2(string)", max_length=1024)


# Create your models here.
class IC(models.Model):
    # id不用管
    # id=models.BigAutoField(verbose_name="id",primary_key=True)
    # to指的是与那张表相连，to_field指表中的那一列 生成数据列UserInfo_id
    keyword = models.CharField(verbose_name="关键字", max_length=16)
    userid = models.ForeignKey(to="Consumers", to_field="id", on_delete=models.CASCADE)
    # lambda1 = models.CharField(verbose_name="lambda1", max_length=1024)
    # lambda2 = models.CharField(verbose_name="lambda2", max_length=1024)
    # r = models.CharField(verbose_name="随机数r", max_length=1024, default="1")
    # q = models.CharField(verbose_name="q", max_length=1024)
    ic1 = models.BinaryField(verbose_name="ic1", max_length=1024)
    ic2 = models.BinaryField(verbose_name="ic2", max_length=1024)
    power = models.DecimalField(verbose_name="能源量", max_digits=10, decimal_places=2, default=0)
    # sign = models.BooleanField(verbose_name="标签", default=False)
    user_time = models.DateTimeField(verbose_name="上传时间", auto_now_add=True)
    type_choices = (
        (1, "供电"),
        (0, "需电"),
    )
    type = models.SmallIntegerField(verbose_name="类型", choices=type_choices, default=0)
    index = models.IntegerField(verbose_name="调度轮数")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['userid', 'index'], name='uc_userid_index')
        ]


class Result(models.Model):
    index = models.IntegerField(verbose_name="调度轮数", unique=True)
    suppliers = models.CharField(verbose_name="供电用户名单", max_length=1024)
    demanders = models.CharField(verbose_name="需电用户名单", max_length=1024)
    supply = models.CharField(verbose_name="实际供电结果", max_length=1024)
    demand = models.CharField(verbose_name="实际得电结果", max_length=1024)


class UserInfo(models.Model):
    """管理员表"""
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    create_time = models.DateField(verbose_name="入职时间")
    # 无约束 depart_did = models.BigIntegerField(verbose_name="部门ID")
    # 有约束
    # -to 与哪张表关联
    # - to_field 表中的哪一列关联
    # django自动

    gender_choice = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choice)
