# Feature Selection Log

**Started:** 2026-05-25T14:03:18

## Config

- `N_TRIALS_PER_ATTEMPT`: 25
- `N_TRIALS_FINAL`: 50
- `IMPROVEMENT_THRESHOLD`: 0.0
- `CV_SPLITS`: 5
- `RANDOM_SEED`: 42
- `SCALE_POS_WEIGHT`: 0.985722
- Starting features (20): ['PromoCode', 'Region', 'AllInclusive', 'PackageType', 'VIP', 'RoomService', 'Dining', 'Retail', 'Spa', 'Entertainment', 'LoyaltyPoints', 'SurveyScore', 'DaysSinceEmail', 'BookingChannel', 'AgeGroup', 'ReferralSource', 'SharedRoom', 'RoomFloor', 'RoomNumber', 'RoomSide']

## Baseline (all 20 features)

- **Baseline CV ROC-AUC:** `0.84331`
- Best params: `{"depth": 4, "learning_rate": 0.178853, "l2_leaf_reg": 0.05975, "bagging_temperature": 0.662522, "random_strength": 0.017654, "border_count": 148, "min_data_in_leaf": 55}`

### Initial feature importance (ascending — least important first):

```
       feature  importance
    SharedRoom    0.000000
           VIP    0.000000
BookingChannel    0.016688
   SurveyScore    0.301703
      AgeGroup    0.734872
   PackageType    1.250501
DaysSinceEmail    1.299044
      RoomSide    2.327446
        Retail    3.446481
 LoyaltyPoints    3.587882
    RoomNumber    5.358133
     RoomFloor    5.501362
     PromoCode    5.714518
   RoomService    6.124599
        Dining    6.674097
ReferralSource    7.664886
        Region    8.762624
  AllInclusive    9.687631
 Entertainment   15.644882
           Spa   15.902652
```

## Round 1 (features: 20, current score: 0.84331)

**10 least-important features this round (re-ranked from current model):**

```
       feature  importance
    SharedRoom    0.000000
           VIP    0.000000
BookingChannel    0.016688
   SurveyScore    0.301703
      AgeGroup    0.734872
   PackageType    1.250501
DaysSinceEmail    1.299044
      RoomSide    2.327446
        Retail    3.446481
 LoyaltyPoints    3.587882
```

### Round 1 — try removing `SharedRoom`
- New CV ROC-AUC: `0.84376` (Δ = `+0.00045`) → **✅ ACCEPT**
- Dropped `SharedRoom`. Remaining features: 19.
- New best params: `{"depth": 5, "learning_rate": 0.037648, "l2_leaf_reg": 4.194646, "bagging_temperature": 0.575162, "random_strength": 0.159323, "border_count": 32, "min_data_in_leaf": 13}`

## Round 2 (features: 19, current score: 0.84376)

**10 least-important features this round (re-ranked from current model):**

```
       feature  importance
           VIP    0.106553
BookingChannel    0.299250
   SurveyScore    0.918250
DaysSinceEmail    1.326613
      AgeGroup    1.490429
   PackageType    1.499698
 LoyaltyPoints    1.554710
      RoomSide    3.162460
        Retail    4.047269
     RoomFloor    5.018862
```

### Round 2 — try removing `VIP`
- New CV ROC-AUC: `0.84193` (Δ = `-0.00183`) → **❌ REJECT**
- Kept `VIP`. Trying next column.

### Round 2 — try removing `BookingChannel`
- New CV ROC-AUC: `0.84392` (Δ = `+0.00016`) → **✅ ACCEPT**
- Dropped `BookingChannel`. Remaining features: 18.
- New best params: `{"depth": 7, "learning_rate": 0.05416, "l2_leaf_reg": 8.102356, "bagging_temperature": 0.95514, "random_strength": 0.40501, "border_count": 160, "min_data_in_leaf": 74}`

## Round 3 (features: 18, current score: 0.84392)

**10 least-important features this round (re-ranked from current model):**

```
       feature  importance
           VIP    0.074004
   SurveyScore    1.896291
   PackageType    1.915822
 LoyaltyPoints    2.544258
DaysSinceEmail    2.563977
      AgeGroup    2.724179
        Retail    3.904170
      RoomSide    4.539956
     RoomFloor    5.714908
        Dining    5.768520
```

### Round 3 — try removing `VIP`
- New CV ROC-AUC: `0.84363` (Δ = `-0.00029`) → **❌ REJECT**
- Kept `VIP`. Trying next column.

### Round 3 — try removing `SurveyScore`
- New CV ROC-AUC: `0.84245` (Δ = `-0.00147`) → **❌ REJECT**
- Kept `SurveyScore`. Trying next column.

### Round 3 — try removing `PackageType`
- New CV ROC-AUC: `0.84046` (Δ = `-0.00346`) → **❌ REJECT**
- Kept `PackageType`. Trying next column.

### Round 3 — try removing `LoyaltyPoints`
- New CV ROC-AUC: `0.84333` (Δ = `-0.00059`) → **❌ REJECT**
- Kept `LoyaltyPoints`. Trying next column.

### Round 3 — try removing `DaysSinceEmail`
- New CV ROC-AUC: `0.84333` (Δ = `-0.00059`) → **❌ REJECT**
- Kept `DaysSinceEmail`. Trying next column.

### Round 3 — try removing `AgeGroup`
- New CV ROC-AUC: `0.84317` (Δ = `-0.00075`) → **❌ REJECT**
- Kept `AgeGroup`. Trying next column.

### Round 3 — try removing `Retail`
- New CV ROC-AUC: `0.83801` (Δ = `-0.00591`) → **❌ REJECT**
- Kept `Retail`. Trying next column.

### Round 3 — try removing `RoomSide`
- New CV ROC-AUC: `0.83686` (Δ = `-0.00706`) → **❌ REJECT**
- Kept `RoomSide`. Trying next column.

### Round 3 — try removing `RoomFloor`
- New CV ROC-AUC: `0.83941` (Δ = `-0.00451`) → **❌ REJECT**
- Kept `RoomFloor`. Trying next column.

### Round 3 — try removing `Dining`
- New CV ROC-AUC: `0.83700` (Δ = `-0.00692`) → **❌ REJECT**
- Kept `Dining`. Trying next column.

### Round 3 — try removing `AllInclusive`
- New CV ROC-AUC: `0.84146` (Δ = `-0.00246`) → **❌ REJECT**
- Kept `AllInclusive`. Trying next column.

### Round 3 — try removing `PromoCode`
- New CV ROC-AUC: `0.83338` (Δ = `-0.01054`) → **❌ REJECT**
- Kept `PromoCode`. Trying next column.

### Round 3 — try removing `RoomService`
- New CV ROC-AUC: `0.83500` (Δ = `-0.00892`) → **❌ REJECT**
- Kept `RoomService`. Trying next column.

### Round 3 — try removing `RoomNumber`
- New CV ROC-AUC: `0.83468` (Δ = `-0.00924`) → **❌ REJECT**
- Kept `RoomNumber`. Trying next column.

### Round 3 — try removing `Entertainment`
- New CV ROC-AUC: `0.82996` (Δ = `-0.01396`) → **❌ REJECT**
- Kept `Entertainment`. Trying next column.

### Round 3 — try removing `ReferralSource`
- New CV ROC-AUC: `0.82707` (Δ = `-0.01685`) → **❌ REJECT**
- Kept `ReferralSource`. Trying next column.

### Round 3 — try removing `Spa`
- New CV ROC-AUC: `0.83001` (Δ = `-0.01391`) → **❌ REJECT**
- Kept `Spa`. Trying next column.

### Round 3 — try removing `Region`
- New CV ROC-AUC: `0.84230` (Δ = `-0.00162`) → **❌ REJECT**
- Kept `Region`. Trying next column.

## Stop — round 3 produced no improvement > 0.0.

## Search summary

- **Final CV ROC-AUC (during search):** `0.84392` (baseline `0.84331`, Δ = `+0.00061`)
- Removed 2 columns in order: `['SharedRoom', 'BookingChannel']`
- Kept 18 columns: `['PromoCode', 'Region', 'AllInclusive', 'PackageType', 'VIP', 'RoomService', 'Dining', 'Retail', 'Spa', 'Entertainment', 'LoyaltyPoints', 'SurveyScore', 'DaysSinceEmail', 'AgeGroup', 'ReferralSource', 'RoomFloor', 'RoomNumber', 'RoomSide']`

## Final re-tune (50 trials on winning feature set)

- Re-tuned CV ROC-AUC: `0.84392` (search result was `0.84392`)
- Re-tuned best params: `{"depth": 7, "learning_rate": 0.05416, "l2_leaf_reg": 8.102356, "bagging_temperature": 0.95514, "random_strength": 0.40501, "border_count": 160, "min_data_in_leaf": 74}`

ℹ️ Re-tune did not beat the search result — falling back to search-result params for the submission.

- **Winning features (18):** `['PromoCode', 'Region', 'AllInclusive', 'PackageType', 'VIP', 'RoomService', 'Dining', 'Retail', 'Spa', 'Entertainment', 'LoyaltyPoints', 'SurveyScore', 'DaysSinceEmail', 'AgeGroup', 'ReferralSource', 'RoomFloor', 'RoomNumber', 'RoomSide']`
- **Winning CV ROC-AUC:** `0.84392`
- **Winning params:** `{"depth": 7, "learning_rate": 0.05416, "l2_leaf_reg": 8.102356, "bagging_temperature": 0.95514, "random_strength": 0.40501, "border_count": 160, "min_data_in_leaf": 74}`

## Submission

- Wrote `submission.csv` (1739 rows)
- Predictions: 844 True, 895 False

**Completed:** 2026-05-25T15:28:44

