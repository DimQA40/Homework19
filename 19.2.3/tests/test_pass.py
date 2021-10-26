import pytest

from app.calculator import Calculator

class TestCalcPass:
    def setup(self):
        self.calc = Calculator

    def test_multiply_calculator_correctly(self):
        assert self.calc.multiply(self, 5, 5) == 25

    def test_division_calculator_correctly(self):
        assert self.calc.division(self, 30, 6) == 5

    def test_subtraction_calculator_correctly(self):
        assert self.calc.subtraction(self, 10, 5) == 5

    def test_adding_calculator_correctly(self):
        assert self.calc.adding(self, 2, 3) == 5