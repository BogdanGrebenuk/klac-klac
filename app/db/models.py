import sqlalchemy as sa


metadata = sa.MetaData()


User = sa.Table(
    'user',
    metadata,
    sa.Column('id', sa.Text, primary_key=True),
    sa.Column('first_name', sa.Text, nullable=False),
    sa.Column('last_name', sa.Text, nullable=False),
    sa.Column('patronymic', sa.Text, nullable=False),
    sa.Column('email', sa.Text, nullable=False, unique=True),
    sa.Column('password', sa.Text, nullable=False),
    sa.Column('role', sa.Text, nullable=False),
    sa.Column('token', sa.Text, nullable=True),
    sa.Column('passenger_id', sa.Text, sa.ForeignKey("passenger.id"), nullable=True),
    sa.Column('driver_id', sa.Text, sa.ForeignKey("driver.id"), nullable=True)
)

Driver = sa.Table(
    'driver',
    metadata,
    sa.Column('id', sa.Text, primary_key=True),
    sa.Column('user_id', sa.Text, sa.ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    sa.Column('car_image', sa.Text,),
)

Passenger = sa.Table(
    'passenger',
    metadata,
    sa.Column('id', sa.Text, primary_key=True),
    sa.Column('user_id', sa.Text, sa.ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
)

Order = sa.Table(
    'order',
    metadata,
    sa.Column('id', sa.Text, primary_key=True),
    sa.Column('from_', sa.Text, nullable=False),
    sa.Column('to', sa.Text, nullable=False),
    sa.Column('status', sa.Text, nullable=False),
    sa.Column('image', sa.Text, nullable=True),
    sa.Column('driver_id', sa.Text, sa.ForeignKey("driver.id", ondelete="CASCADE"), nullable=True),
    sa.Column('passenger_id', sa.Text, sa.ForeignKey("passenger.id", ondelete="CASCADE"), nullable=False),
    sa.Column('geolocation', sa.Text, nullable=True),
)

Agreement = sa.Table(
    'agreement',
    metadata,
    sa.Column('id', sa.Text, primary_key=True),
    sa.Column('driver_id', sa.Text, sa.ForeignKey("driver.id", ondelete="CASCADE"), nullable=False),
    sa.Column('order_id', sa.Text, sa.ForeignKey("order.id", ondelete="CASCADE"), nullable=False),
)

BlackList = sa.Table(
    'blacklist',
    metadata,
    sa.Column('ban_driver_id', sa.Text, sa.ForeignKey("driver.id", ondelete="CASCADE"), nullable=False),
    sa.Column('passenger_id', sa.Text, sa.ForeignKey("passenger.id", ondelete="CASCADE"), nullable=False),
)


WhiteList = sa.Table(
    'whitelist',
    metadata,
    sa.Column('driver_id', sa.Text, sa.ForeignKey("driver.id", ondelete="CASCADE"), nullable=False),
    sa.Column('passenger_id', sa.Text, sa.ForeignKey("passenger.id", ondelete="CASCADE"), nullable=False),
)