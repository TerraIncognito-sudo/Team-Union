# Feature Selection Log

**Started:** 2026-05-23T20:25:50

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

**10 least-important features this round (re-ranked from current model):**

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
```

### Round 1 — try removing `RoomFloor_T`
- New CV ROC-AUC: `0.82269` (Δ = `+0.00155`) → **❌ REJECT**
- Kept `RoomFloor_T`. Trying next column.

### Round 1 — try removing `ReferralSource_Newspaper`
- New CV ROC-AUC: `0.82472` (Δ = `+0.00357`) → **✅ ACCEPT**
- Dropped `ReferralSource_Newspaper`. Remaining features: 58.
- New best params: `{"depth": 6, "learning_rate": 0.019284, "l2_leaf_reg": 0.068217, "bagging_temperature": 0.811071, "random_strength": 0.08571, "border_count": 222, "min_data_in_leaf": 14}`

## Round 2 (features: 58, current score: 0.82472)

**10 least-important features this round (re-ranked from current model):**

```
                 feature  importance
        RoomSide_Unknown    0.000000
             RoomFloor_T    0.000000
       ReferralSource_TV    0.000000
ReferralSource_Pinterest    0.007395
 ReferralSource_Magazine    0.022594
 ReferralSource_LinkedIn    0.031043
       RoomFloor_Unknown    0.033423
              SharedRoom    0.046705
             RoomFloor_D    0.047133
   ReferralSource_Google    0.060295
```

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
- New CV ROC-AUC: `0.82315` (Δ = `-0.00156`) → **❌ REJECT**
- Kept `ReferralSource_Pinterest`. Trying next column.

### Round 2 — try removing `ReferralSource_Magazine`
- New CV ROC-AUC: `0.82269` (Δ = `-0.00203`) → **❌ REJECT**
- Kept `ReferralSource_Magazine`. Trying next column.

### Round 2 — try removing `ReferralSource_LinkedIn`
- New CV ROC-AUC: `0.82270` (Δ = `-0.00202`) → **❌ REJECT**
- Kept `ReferralSource_LinkedIn`. Trying next column.

### Round 2 — try removing `RoomFloor_Unknown`
- New CV ROC-AUC: `0.82413` (Δ = `-0.00059`) → **❌ REJECT**
- Kept `RoomFloor_Unknown`. Trying next column.

### Round 2 — try removing `SharedRoom`
- New CV ROC-AUC: `0.82171` (Δ = `-0.00300`) → **❌ REJECT**
- Kept `SharedRoom`. Trying next column.

### Round 2 — try removing `RoomFloor_D`
- New CV ROC-AUC: `0.82313` (Δ = `-0.00159`) → **❌ REJECT**
- Kept `RoomFloor_D`. Trying next column.

### Round 2 — try removing `ReferralSource_Google`
- New CV ROC-AUC: `0.82255` (Δ = `-0.00217`) → **❌ REJECT**
- Kept `ReferralSource_Google`. Trying next column.

### Round 2 — try removing `ReferralSource_Radio`
- New CV ROC-AUC: `0.82227` (Δ = `-0.00245`) → **❌ REJECT**
- Kept `ReferralSource_Radio`. Trying next column.

### Round 2 — try removing `AgeGroup_Unknown`
- New CV ROC-AUC: `0.82272` (Δ = `-0.00199`) → **❌ REJECT**
- Kept `AgeGroup_Unknown`. Trying next column.

### Round 2 — try removing `ReferralSource_Facebook`
- New CV ROC-AUC: `0.82085` (Δ = `-0.00387`) → **❌ REJECT**
- Kept `ReferralSource_Facebook`. Trying next column.

### Round 2 — try removing `AgeGroup_Senior`
- New CV ROC-AUC: `0.82325` (Δ = `-0.00146`) → **❌ REJECT**
- Kept `AgeGroup_Senior`. Trying next column.

### Round 2 — try removing `BookingChannel_Phone`
- New CV ROC-AUC: `0.82285` (Δ = `-0.00187`) → **❌ REJECT**
- Kept `BookingChannel_Phone`. Trying next column.

### Round 2 — try removing `BookingChannel_Mobile`
- New CV ROC-AUC: `0.82140` (Δ = `-0.00332`) → **❌ REJECT**
- Kept `BookingChannel_Mobile`. Trying next column.

### Round 2 — try removing `VIP`
- New CV ROC-AUC: `0.82298` (Δ = `-0.00174`) → **❌ REJECT**
- Kept `VIP`. Trying next column.

### Round 2 — try removing `Region_Unknown`
- New CV ROC-AUC: `0.82429` (Δ = `-0.00042`) → **❌ REJECT**
- Kept `Region_Unknown`. Trying next column.

### Round 2 — try removing `BookingChannel_Website`
- New CV ROC-AUC: `0.82199` (Δ = `-0.00273`) → **❌ REJECT**
- Kept `BookingChannel_Website`. Trying next column.

### Round 2 — try removing `BookingYear`
- New CV ROC-AUC: `0.82426` (Δ = `-0.00045`) → **❌ REJECT**
- Kept `BookingYear`. Trying next column.

### Round 2 — try removing `PackageType_NoPackage`
- New CV ROC-AUC: `0.82141` (Δ = `-0.00330`) → **❌ REJECT**
- Kept `PackageType_NoPackage`. Trying next column.

### Round 2 — try removing `ReferralSource_Twitter`
- New CV ROC-AUC: `0.82182` (Δ = `-0.00289`) → **❌ REJECT**
- Kept `ReferralSource_Twitter`. Trying next column.

### Round 2 — try removing `ReferralSource_Flyer`
- New CV ROC-AUC: `0.82242` (Δ = `-0.00229`) → **❌ REJECT**
- Kept `ReferralSource_Flyer`. Trying next column.

### Round 2 — try removing `ReferralSource_Instagram`
- New CV ROC-AUC: `0.82369` (Δ = `-0.00102`) → **❌ REJECT**
- Kept `ReferralSource_Instagram`. Trying next column.

### Round 2 — try removing `AgeGroup_Young`
- New CV ROC-AUC: `0.82313` (Δ = `-0.00159`) → **❌ REJECT**
- Kept `AgeGroup_Young`. Trying next column.

### Round 2 — try removing `BookingChannel_TravelAgent`
- New CV ROC-AUC: `0.82373` (Δ = `-0.00099`) → **❌ REJECT**
- Kept `BookingChannel_TravelAgent`. Trying next column.

### Round 2 — try removing `PackageType_Wellness`
- New CV ROC-AUC: `0.82399` (Δ = `-0.00072`) → **❌ REJECT**
- Kept `PackageType_Wellness`. Trying next column.

### Round 2 — try removing `ReferralSource_Podcast`
- New CV ROC-AUC: `0.82142` (Δ = `-0.00330`) → **❌ REJECT**
- Kept `ReferralSource_Podcast`. Trying next column.

### Round 2 — try removing `AgeGroup_Middle`
- New CV ROC-AUC: `0.82199` (Δ = `-0.00272`) → **❌ REJECT**
- Kept `AgeGroup_Middle`. Trying next column.

### Round 2 — try removing `RoomFloor_B`
- New CV ROC-AUC: `0.82558` (Δ = `+0.00087`) → **❌ REJECT**
- Kept `RoomFloor_B`. Trying next column.

### Round 2 — try removing `PackageType_Relaxation`
- New CV ROC-AUC: `0.82086` (Δ = `-0.00385`) → **❌ REJECT**
- Kept `PackageType_Relaxation`. Trying next column.

### Round 2 — try removing `ReferralSource_Yelp`
- New CV ROC-AUC: `0.82113` (Δ = `-0.00358`) → **❌ REJECT**
- Kept `ReferralSource_Yelp`. Trying next column.

### Round 2 — try removing `RoomFloor_E`
- New CV ROC-AUC: `0.82228` (Δ = `-0.00243`) → **❌ REJECT**
- Kept `RoomFloor_E`. Trying next column.

### Round 2 — try removing `SurveyScore`
- New CV ROC-AUC: `0.82185` (Δ = `-0.00287`) → **❌ REJECT**
- Kept `SurveyScore`. Trying next column.

### Round 2 — try removing `ReferralSource_Email`
- New CV ROC-AUC: `0.81973` (Δ = `-0.00499`) → **❌ REJECT**
- Kept `ReferralSource_Email`. Trying next column.

### Round 2 — try removing `ReferralSource_TripAdvisor`
- New CV ROC-AUC: `0.81882` (Δ = `-0.00590`) → **❌ REJECT**
- Kept `ReferralSource_TripAdvisor`. Trying next column.

### Round 2 — try removing `ReferralSource_YouTube`
- New CV ROC-AUC: `0.82397` (Δ = `-0.00074`) → **❌ REJECT**
- Kept `ReferralSource_YouTube`. Trying next column.

### Round 2 — try removing `RoomFloor_C`
- New CV ROC-AUC: `0.82168` (Δ = `-0.00304`) → **❌ REJECT**
- Kept `RoomFloor_C`. Trying next column.

### Round 2 — try removing `DaysSinceEmail`
- New CV ROC-AUC: `0.82180` (Δ = `-0.00292`) → **❌ REJECT**
- Kept `DaysSinceEmail`. Trying next column.

### Round 2 — try removing `Dining`
- New CV ROC-AUC: `0.81897` (Δ = `-0.00574`) → **❌ REJECT**
- Kept `Dining`. Trying next column.

### Round 2 — try removing `Retail`
- New CV ROC-AUC: `0.81549` (Δ = `-0.00922`) → **❌ REJECT**
- Kept `Retail`. Trying next column.

### Round 2 — try removing `ReferralSource_TikTok`
- New CV ROC-AUC: `0.82136` (Δ = `-0.00336`) → **❌ REJECT**
- Kept `ReferralSource_TikTok`. Trying next column.

### Round 2 — try removing `BookingMonth`
- New CV ROC-AUC: `0.82057` (Δ = `-0.00415`) → **❌ REJECT**
- Kept `BookingMonth`. Trying next column.

### Round 2 — try removing `RoomFloor_G`
- New CV ROC-AUC: `0.82268` (Δ = `-0.00204`) → **❌ REJECT**
- Kept `RoomFloor_G`. Trying next column.

### Round 2 — try removing `Region_AsiaPacific`
- New CV ROC-AUC: `0.81967` (Δ = `-0.00505`) → **❌ REJECT**
- Kept `Region_AsiaPacific`. Trying next column.

### Round 2 — try removing `LoyaltyPoints`
- New CV ROC-AUC: `0.82285` (Δ = `-0.00187`) → **❌ REJECT**
- Kept `LoyaltyPoints`. Trying next column.

### Round 2 — try removing `ReferralSource_Friend`
- New CV ROC-AUC: `0.81730` (Δ = `-0.00741`) → **❌ REJECT**
- Kept `ReferralSource_Friend`. Trying next column.

### Round 2 — try removing `RoomSide_S`
- New CV ROC-AUC: `0.81448` (Δ = `-0.01023`) → **❌ REJECT**
- Kept `RoomSide_S`. Trying next column.

### Round 2 — try removing `RoomService`
- New CV ROC-AUC: `0.81627` (Δ = `-0.00845`) → **❌ REJECT**
- Kept `RoomService`. Trying next column.

### Round 2 — try removing `AgeGroup_Minor`
- New CV ROC-AUC: `0.81999` (Δ = `-0.00473`) → **❌ REJECT**
- Kept `AgeGroup_Minor`. Trying next column.

### Round 2 — try removing `PromoCode_PromoA`
- New CV ROC-AUC: `0.81142` (Δ = `-0.01329`) → **❌ REJECT**
- Kept `PromoCode_PromoA`. Trying next column.

### Round 2 — try removing `RoomFloor_F`
- New CV ROC-AUC: `0.82328` (Δ = `-0.00144`) → **❌ REJECT**
- Kept `RoomFloor_F`. Trying next column.

### Round 2 — try removing `PromoCode_PromoB`
- New CV ROC-AUC: `0.81425` (Δ = `-0.01046`) → **❌ REJECT**
- Kept `PromoCode_PromoB`. Trying next column.

### Round 2 — try removing `Entertainment`
- New CV ROC-AUC: `0.81293` (Δ = `-0.01179`) → **❌ REJECT**
- Kept `Entertainment`. Trying next column.

### Round 2 — try removing `RoomNumber`
- New CV ROC-AUC: `0.81404` (Δ = `-0.01068`) → **❌ REJECT**
- Kept `RoomNumber`. Trying next column.

### Round 2 — try removing `Region_Europe`
- New CV ROC-AUC: `0.82283` (Δ = `-0.00188`) → **❌ REJECT**
- Kept `Region_Europe`. Trying next column.

### Round 2 — try removing `Spa`
- New CV ROC-AUC: `0.81064` (Δ = `-0.01408`) → **❌ REJECT**
- Kept `Spa`. Trying next column.

### Round 2 — try removing `AllInclusive`
- New CV ROC-AUC: `0.79812` (Δ = `-0.02660`) → **❌ REJECT**
- Kept `AllInclusive`. Trying next column.

## Stop — round 2 produced no improvement > 0.002.

## Search summary

- **Final CV ROC-AUC (during search):** `0.82472` (baseline `0.82114`, Δ = `+0.00357`)
- Removed 1 columns in order: `['ReferralSource_Newspaper']`
- Kept 58 columns: `['AllInclusive', 'VIP', 'RoomService', 'Dining', 'Retail', 'Spa', 'Entertainment', 'LoyaltyPoints', 'SurveyScore', 'DaysSinceEmail', 'SharedRoom', 'RoomNumber', 'BookingMonth', 'BookingYear', 'PromoCode_PromoA', 'PromoCode_PromoB', 'Region_AsiaPacific', 'Region_Europe', 'Region_Unknown', 'PackageType_NoPackage', 'PackageType_Relaxation', 'PackageType_Wellness', 'AgeGroup_Middle', 'AgeGroup_Minor', 'AgeGroup_Senior', 'AgeGroup_Unknown', 'AgeGroup_Young', 'RoomFloor_B', 'RoomFloor_C', 'RoomFloor_D', 'RoomFloor_E', 'RoomFloor_F', 'RoomFloor_G', 'RoomFloor_T', 'RoomFloor_Unknown', 'RoomSide_S', 'RoomSide_Unknown', 'BookingChannel_Mobile', 'BookingChannel_Phone', 'BookingChannel_TravelAgent', 'BookingChannel_Website', 'ReferralSource_Email', 'ReferralSource_Facebook', 'ReferralSource_Flyer', 'ReferralSource_Friend', 'ReferralSource_Google', 'ReferralSource_Instagram', 'ReferralSource_LinkedIn', 'ReferralSource_Magazine', 'ReferralSource_Pinterest', 'ReferralSource_Podcast', 'ReferralSource_Radio', 'ReferralSource_TV', 'ReferralSource_TikTok', 'ReferralSource_TripAdvisor', 'ReferralSource_Twitter', 'ReferralSource_Yelp', 'ReferralSource_YouTube']`

## Final re-tune (50 trials on winning feature set)

- Re-tuned CV ROC-AUC: `0.82472` (search result was `0.82472`)
- Re-tuned best params: `{"depth": 6, "learning_rate": 0.019284, "l2_leaf_reg": 0.068217, "bagging_temperature": 0.811071, "random_strength": 0.08571, "border_count": 222, "min_data_in_leaf": 14}`

ℹ️ Re-tune did not beat the search result — falling back to search-result params for the submission.

- **Winning features (58):** `['AllInclusive', 'VIP', 'RoomService', 'Dining', 'Retail', 'Spa', 'Entertainment', 'LoyaltyPoints', 'SurveyScore', 'DaysSinceEmail', 'SharedRoom', 'RoomNumber', 'BookingMonth', 'BookingYear', 'PromoCode_PromoA', 'PromoCode_PromoB', 'Region_AsiaPacific', 'Region_Europe', 'Region_Unknown', 'PackageType_NoPackage', 'PackageType_Relaxation', 'PackageType_Wellness', 'AgeGroup_Middle', 'AgeGroup_Minor', 'AgeGroup_Senior', 'AgeGroup_Unknown', 'AgeGroup_Young', 'RoomFloor_B', 'RoomFloor_C', 'RoomFloor_D', 'RoomFloor_E', 'RoomFloor_F', 'RoomFloor_G', 'RoomFloor_T', 'RoomFloor_Unknown', 'RoomSide_S', 'RoomSide_Unknown', 'BookingChannel_Mobile', 'BookingChannel_Phone', 'BookingChannel_TravelAgent', 'BookingChannel_Website', 'ReferralSource_Email', 'ReferralSource_Facebook', 'ReferralSource_Flyer', 'ReferralSource_Friend', 'ReferralSource_Google', 'ReferralSource_Instagram', 'ReferralSource_LinkedIn', 'ReferralSource_Magazine', 'ReferralSource_Pinterest', 'ReferralSource_Podcast', 'ReferralSource_Radio', 'ReferralSource_TV', 'ReferralSource_TikTok', 'ReferralSource_TripAdvisor', 'ReferralSource_Twitter', 'ReferralSource_Yelp', 'ReferralSource_YouTube']`
- **Winning CV ROC-AUC:** `0.82472`
- **Winning params:** `{"depth": 6, "learning_rate": 0.019284, "l2_leaf_reg": 0.068217, "bagging_temperature": 0.811071, "random_strength": 0.08571, "border_count": 222, "min_data_in_leaf": 14}`

## Submission

- Wrote `submission.csv` (1739 rows)
- Predictions: 809 True, 930 False

**Completed:** 2026-05-23T22:08:57

