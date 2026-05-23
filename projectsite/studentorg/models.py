from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class College(BaseModel):
    college_name = models.CharField('category name', max_length=150)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.college_name


class Program(BaseModel):
    prog_name = models.CharField('caliber / series', max_length=150)
    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE,
        verbose_name='category',
    )

    class Meta:
        verbose_name = 'caliber'
        verbose_name_plural = 'calibers'

    def __str__(self):
        return self.prog_name


class Organization(BaseModel):
    name = models.CharField('firearm name', max_length=250)
    college = models.ForeignKey(
        College,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='category',
    )
    description = models.CharField('description', max_length=500)
    price = models.DecimalField(
        'price (USD)',
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    class Meta:
        verbose_name = 'firearm'
        verbose_name_plural = 'firearms'

    def __str__(self):
        return self.name


class Student(BaseModel):
    student_id = models.CharField('customer ID', max_length=15)
    lastname = models.CharField('last name', max_length=25)
    firstname = models.CharField('first name', max_length=25)
    middlename = models.CharField('middle name', max_length=25, blank=True, null=True)
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        verbose_name='preferred caliber',
    )

    class Meta:
        verbose_name = 'customer'
        verbose_name_plural = 'customers'

    def __str__(self):
        return f"{self.lastname}, {self.firstname}"


class OrgMember(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='customer')
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name='firearm',
    )
    date_joined = models.DateField('sale date')

    class Meta:
        verbose_name = 'sale'
        verbose_name_plural = 'sales'

    def __str__(self):
        return f"{self.student} - {self.organization}"

