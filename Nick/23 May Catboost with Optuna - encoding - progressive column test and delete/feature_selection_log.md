# Feature Selection Log

**Started:** 2026-05-23T19:17:23

## Config

- `N_TRIALS_PER_ATTEMPT`: 25
- `N_TRIALS_FINAL`: 50
- `IMPROVEMENT_THRESHOLD`: 0.002
- `CV_SPLITS`: 5
- `RANDOM_SEED`: 42
- `SCALE_POS_WEIGHT`: 0.985722
- Starting features (59): ['AllInclusive', 'VIP', 'RoomService', 'Dining', 'Retail', 'Spa', 'Entertainment', 'LoyaltyPoints', 'SurveyScore', 'DaysSinceEmail', 'SharedRoom', 'RoomNumber', 'BookingMonth', 'BookingYear', 'PromoCode_PromoA', 'PromoCode_PromoB', 'Region_AsiaPacific', 'Region_Europe', 'Region_Unknown', 'PackageType_NoPackage', 'PackageType_Relaxation', 'PackageType_Wellness', 'AgeGroup_Middle', 'AgeGroup_Minor', 'AgeGroup_Senior', 'AgeGroup_Unknown', 'AgeGroup_Young', 'RoomFloor_B', 'RoomFloor_C', 'RoomFloor_D', 'RoomFloor_E', 'RoomFloor_F', 'RoomFloor_G', 'RoomFloor_T', 'RoomFloor_Unknown', 'RoomSide_S', 'RoomSide_Unknown', 'BookingChannel_Mobile', 'BookingChannel_Phone', 'BookingChannel_TravelAgent', 'BookingChannel_Website', 'ReferralSource_Email', 'ReferralSource_Facebook', 'ReferralSource_Flyer', 'ReferralSource_Friend', 'ReferralSource_Google', 'ReferralSource_Instagram', 'ReferralSource_LinkedIn', 'ReferralSource_Magazine', 'ReferralSource_Newspaper', 'ReferralSource_Pinterest', 'ReferralSource_Podcast', 'ReferralSource_Radio', 'ReferralSource_TV', 'ReferralSource_TikTok', 'ReferralSource_TripAdvisor', 'ReferralSource_Twitter', 'ReferralSource_Yelp', 'ReferralSource_YouTube']

## Baseline (all 59 features)

- **Baseline CV ROC-AUC:** `0.82114`
- Best params: `{"depth": 8, "learning_rate": 0.013365, "l2_leaf_reg": 3.741304, "bagging_temperature": 0.761061, "random_strength": 0.442185, "border_count": 247, "min_data_in_leaf": 14}`

### Initial feature importance (ascending — least important first):

```
                   feature  importance
               RoomFloor_T    0.000000
  ReferralSource_Newspaper    0.000000
  ReferralSource_Pinterest    0.002052
   ReferralSource_LinkedIn    0.002739
               RoomFloor_D    0.008163
   ReferralSource_Magazine    0.011606
         RoomFloor_Unknown    0.015727
                SharedRoom    0.016172
          RoomSide_Unknown    0.020169
      ReferralSource_Radio    0.021086
         ReferralSource_TV    0.022668
          AgeGroup_Unknown    0.033597
                       VIP    0.034758
      ReferralSource_Flyer    0.046729
     PackageType_NoPackage    0.067658
            Region_Unknown    0.083768
    ReferralSource_Twitter    0.097912
     ReferralSource_Google    0.108561
    ReferralSource_Podcast    0.128671
           AgeGroup_Senior    0.177478
   ReferralSource_Facebook    0.234227
     BookingChannel_Mobile    0.240506
      BookingChannel_Phone    0.275247
  ReferralSource_Instagram    0.329234
    BookingChannel_Website    0.364795
      PackageType_Wellness    0.383718
            AgeGroup_Young    0.389945
               RoomFloor_B    0.419160
               BookingYear    0.550587
           AgeGroup_Middle    0.610881
BookingChannel_TravelAgent    0.611240
    ReferralSource_YouTube    0.643599
       ReferralSource_Yelp    0.698734
               RoomFloor_E    0.789548
    PackageType_Relaxation    0.944038
               RoomFloor_C    1.023438
ReferralSource_TripAdvisor    1.399586
     ReferralSource_TikTok    1.462531
      ReferralSource_Email    1.509827
               SurveyScore    1.963229
                    Retail    2.074467
            DaysSinceEmail    2.245464
               RoomFloor_G    2.322610
        Region_AsiaPacific    2.379323
                    Dining    2.395790
             LoyaltyPoints    2.432086
            AgeGroup_Minor    2.456085
               RoomService    2.618653
              BookingMonth    2.647439
     ReferralSource_Friend    3.237497
               RoomFloor_F    3.427832
             Entertainment    3.437499
                RoomSide_S    3.786313
          PromoCode_PromoA    4.085422
          PromoCode_PromoB    4.238447
                       Spa    5.085824
                RoomNumber    6.001174
             Region_Europe    8.142989
              AllInclusive   21.241505
```

## Round 1 (features: 59, current score: 0.82114)

### Round 1 — try removing `RoomFloor_T`
- New CV ROC-AUC: `0.82269` (Δ = `+0.00155`) → **❌ REJECT**
- Kept `RoomFloor_T`. Trying next column.

### Round 1 — try removing `ReferralSource_Newspaper`
- New CV ROC-AUC: `0.82472` (Δ = `+0.00357`) → **✅ ACCEPT**
- Dropped `ReferralSource_Newspaper`. Remaining features: 58.
- New best params: `{"depth": 6, "learning_rate": 0.019284, "l2_leaf_reg": 0.068217, "bagging_temperature": 0.811071, "random_strength": 0.08571, "border_count": 222, "min_data_in_leaf": 14}`

## Round 2 (features: 58, current score: 0.82472)

### Round 2 — try removing `RoomSide_Unknown`
- New CV ROC-AUC: `0.82413` (Δ = `-0.00059`) → **❌ REJECT**
- Kept `RoomSide_Unknown`. Trying next column.

### Round 2 — try removing `RoomFloor_T`
- New CV ROC-AUC: `0.82270` (Δ = `-0.00202`) → **❌ REJECT**
- Kept `RoomFloor_T`. Trying next column.

### Round 2 — try removing `ReferralSource_TV`
- New CV ROC-AUC: `0.82298` (Δ = `-0.00173`) → **❌ REJECT**
- Kept `ReferralSource_TV`. Trying next column.

### Round 2 — try removing `ReferralSource_Pinterest`
