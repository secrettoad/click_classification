import pytest
from sklearn.linear_model import LogisticRegression
import dill
import pandas as pd
import pathlib


@pytest.fixture
def test_model(test_meta):
    model = LogisticRegression(**test_meta['params'])
    model.fit(pd.DataFrame([[1]*len(test_meta['features'])]*10, columns=test_meta['features']), pd.Series([0]*5 + [1]*5))
    artifact_path = pathlib.Path(pathlib.Path(__file__).parent.parent, 'artifacts')
    with open('{}/test_model.pkl'.format(str(artifact_path)), 'wb') as f:
        dill.dump(model, f)
    return model


@pytest.fixture
def test_meta():
    return {"params": {"C": 1.0, "class_weight": None, "dual": False, "fit_intercept": True, "intercept_scaling": 1, "l1_ratio": None, "max_iter": 100, "multi_class": "auto", "n_jobs": None, "penalty": "l2", "random_state": None, "solver": "lbfgs", "tol": 0.0001, "verbose": 0, "warm_start": False}, "features": ["apr", "lender_id", "requested", "annual_income", "loan_purpose_auto", "loan_purpose_auto_purchase", "loan_purpose_auto_refinance", "loan_purpose_baby", "loan_purpose_boat", "loan_purpose_business", "loan_purpose_car_repair", "loan_purpose_cosmetic", "loan_purpose_credit_card_refi", "loan_purpose_debt_consolidation", "loan_purpose_emergency", "loan_purpose_green", "loan_purpose_home_improvement", "loan_purpose_home_purchase", "loan_purpose_household_expenses", "loan_purpose_large_purchases", "loan_purpose_life_event", "loan_purpose_medical_dental", "loan_purpose_motorcycle", "loan_purpose_moving_relocation", "loan_purpose_other", "loan_purpose_special_occasion", "loan_purpose_student_loan", "loan_purpose_student_loan_refi", "loan_purpose_taxes", "loan_purpose_unknown", "loan_purpose_vacation", "loan_purpose_wedding", "credit_excellent", "credit_fair", "credit_good", "credit_limited", "credit_poor", "credit_unknown"]}


