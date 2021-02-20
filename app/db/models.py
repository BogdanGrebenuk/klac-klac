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
    sa.Column('user_id', sa.Text, sa.ForeignKey("user.id"), nullable=False),
)

Passenger = sa.Table(
    'passenger',
    metadata,
    sa.Column('id', sa.Text, primary_key=True),
    sa.Column('user_id', sa.Text, sa.ForeignKey("user.id"), nullable=False),
)

Agreement = sa.Table(
    'agreement',
    metadata,
    sa.Column('id', sa.Text, primary_key=True),
    sa.Column('driver_id', sa.Text, sa.ForeignKey("driver.id"), nullable=False),
    sa.Column('passenger_id', sa.Text, sa.ForeignKey("passenger.id"), nullable=False),
)

Order = sa.Table(
    'order',
    metadata,
    sa.Column('id', sa.Text, primary_key=True),
    sa.Column('from_', sa.Text, nullable=False),
    sa.Column('to', sa.Text, nullable=False),
    sa.Column('status', sa.Text, nullable=False),
    sa.Column('driver_id', sa.Text, sa.ForeignKey("driver.id"), nullable=True),
    sa.Column('passenger_id', sa.Text, sa.ForeignKey("passenger.id"), nullable=False),
)