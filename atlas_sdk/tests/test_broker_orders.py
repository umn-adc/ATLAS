import msgspec
import pytest

from atlas_sdk.brokers.base import BrokerOrders


class FakeOrder(msgspec.Struct, tag="fake"):
    symbol: str


class FakeUpdate(msgspec.Struct):
    status: str


def test_order_tag_must_match_broker_name():
    with pytest.raises(TypeError):

        class Mismatched(BrokerOrders[FakeOrder, FakeUpdate]):  # pyright: ignore[reportUnusedClass]
            name = "other"
            version = 1
            order_type = FakeOrder
            update_type = FakeUpdate


def test_missing_required_method_cannot_be_created():
    class Incomplete(BrokerOrders[FakeOrder, FakeUpdate]):
        name = "fake"
        version = 1
        order_type = FakeOrder
        update_type = FakeUpdate

    with pytest.raises(TypeError):
        Incomplete()  # pyright: ignore[reportAbstractUsage]
