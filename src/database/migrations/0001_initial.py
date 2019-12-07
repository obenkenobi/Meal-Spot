# Generated by Django 2.2.6 on 2019-12-03 02:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.TextField()),
                ('apt', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakotsa'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2)),
                ('zip_code', models.IntegerField(validators=[django.core.validators.MaxValueValidator(99999)])),
            ],
        ),
        migrations.CreateModel(
            name='Cook',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('status', models.CharField(choices=[('L', 'Laid Off'), ('N', 'Not Hired'), ('H', 'Hired')], default='N', max_length=2)),
                ('warnings', models.IntegerField(default=0)),
                ('food_drops', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Deliverer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('status', models.CharField(choices=[('L', 'Laid Off'), ('N', 'Not Hired'), ('H', 'Hired')], default='N', max_length=2)),
                ('warnings', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PE', 'Pending'), ('PR', 'Prepared'), ('D', 'Delivered')], default='PE', max_length=2)),
                ('delivery_rating', models.IntegerField(null=True)),
                ('customer_rating', models.IntegerField(null=True)),
                ('total_price', models.FloatField(default=0)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=10, null=True, validators=[django.core.validators.RegexValidator('^\\d{10}$')])),
                ('description', models.TextField(null=True)),
                ('manager', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.Manager')),
            ],
        ),
        migrations.CreateModel(
            name='Salesperson',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('status', models.CharField(choices=[('L', 'Laid Off'), ('N', 'Not Hired'), ('H', 'Hired')], default='N', max_length=2)),
                ('warnings', models.IntegerField(default=0)),
                ('commission', models.FloatField(default=100)),
                ('restaurant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.Restaurant')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SupplyOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_description', models.TextField()),
                ('price', models.FloatField()),
                ('supply_rating', models.FloatField(default=0)),
                ('cook', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.Cook')),
                ('salesperson', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.Salesperson')),
            ],
        ),
        migrations.CreateModel(
            name='Order_Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('isFinished', models.BooleanField(default=False)),
                ('food_rating', models.IntegerField(default=0)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='database.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('vip_free', models.BooleanField(default=False)),
                ('avg_rating', models.FloatField(default=0)),
                ('cook', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='database.Cook')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryBid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('win', models.BooleanField(default=False)),
                ('deliverer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Deliverer')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Order')),
            ],
        ),
        migrations.AddField(
            model_name='deliverer',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.Restaurant'),
        ),
        migrations.CreateModel(
            name='CustomerStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('B', 'Blacklisted'), ('N', 'Not Registered'), ('R', 'Registered'), ('V', 'VIP'), ('P', 'Pending')], default='N', max_length=2)),
                ('order_count', models.IntegerField(default=0)),
                ('avg_rating', models.FloatField(default=0)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.Customer')),
                ('restaurant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.Restaurant')),
            ],
        ),
        migrations.AddField(
            model_name='cook',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.Restaurant'),
        ),
        migrations.CreateModel(
            name='RestaurantAddress',
            fields=[
                ('address_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='database.Address')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Restaurant')),
            ],
            bases=('database.address',),
        ),
        migrations.CreateModel(
            name='CustomerAddress',
            fields=[
                ('address_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='database.Address')),
                ('default', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Customer')),
            ],
            bases=('database.address',),
        ),
    ]
