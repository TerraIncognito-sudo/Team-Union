# Feature Selection Log

**Started:** 2026-05-24T09:31:40

## Config

- `N_TRIALS_PER_ATTEMPT`: 25
- `N_TRIALS_FINAL`: 50
- `IMPROVEMENT_THRESHOLD`: 0.0
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
- New CV ROC-AUC: `0.82269` (Δ = `+0.00155`) → **✅ ACCEPT**
- Dropped `RoomFloor_T`. Remaining features: 58.
- New best params: `{"depth": 4, "learning_rate": 0.178853, "l2_leaf_reg": 0.05975, "bagging_temperature": 0.662522, "random_strength": 0.017654, "border_count": 148, "min_data_in_leaf": 55}`

## Round 2 (features: 58, current score: 0.82269)

**10 least-important features this round (re-ranked from current model):**

```
                 feature  importance
 ReferralSource_LinkedIn         0.0
             RoomFloor_D         0.0
        AgeGroup_Unknown         0.0
   ReferralSource_Google         0.0
  BookingChannel_Website         0.0
   PackageType_NoPackage         0.0
ReferralSource_Instagram         0.0
 ReferralSource_Facebook         0.0
 ReferralSource_Magazine         0.0
        RoomSide_Unknown         0.0
```

### Round 2 — try removing `ReferralSource_LinkedIn`
- New CV ROC-AUC: `0.82240` (Δ = `-0.00029`) → **❌ REJECT**
- Kept `ReferralSource_LinkedIn`. Trying next column.

### Round 2 — try removing `RoomFloor_D`
- New CV ROC-AUC: `0.82272` (Δ = `+0.00003`) → **✅ ACCEPT**
- Dropped `RoomFloor_D`. Remaining features: 57.
- New best params: `{"depth": 7, "learning_rate": 0.034543, "l2_leaf_reg": 0.066037, "bagging_temperature": 0.877024, "random_strength": 0.090772, "border_count": 154, "min_data_in_leaf": 48}`

## Round 3 (features: 57, current score: 0.82272)

**10 least-important features this round (re-ranked from current model):**

```
                 feature  importance
        RoomSide_Unknown    0.000000
       ReferralSource_TV    0.000000
ReferralSource_Newspaper    0.000000
              SharedRoom    0.000000
ReferralSource_Pinterest    0.013095
 ReferralSource_LinkedIn    0.072947
    ReferralSource_Radio    0.074835
                     VIP    0.075254
       RoomFloor_Unknown    0.091027
   ReferralSource_Google    0.096233
```

### Round 3 — try removing `RoomSide_Unknown`
- New CV ROC-AUC: `0.82329` (Δ = `+0.00057`) → **✅ ACCEPT**
- Dropped `RoomSide_Unknown`. Remaining features: 56.
- New best params: `{"depth": 7, "learning_rate": 0.045462, "l2_leaf_reg": 4.78886, "bagging_temperature": 0.878758, "random_strength": 0.107512, "border_count": 178, "min_data_in_leaf": 24}`

## Round 4 (features: 56, current score: 0.82329)

**10 least-important features this round (re-ranked from current model):**

```
                 feature  importance
       ReferralSource_TV    0.000000
ReferralSource_Newspaper    0.000000
 ReferralSource_Magazine    0.000000
ReferralSource_Pinterest    0.007007
 ReferralSource_LinkedIn    0.008054
    ReferralSource_Radio    0.011384
        AgeGroup_Unknown    0.017346
              SharedRoom    0.023086
       RoomFloor_Unknown    0.044962
    BookingChannel_Phone    0.060388
```

### Round 4 — try removing `ReferralSource_TV`
- New CV ROC-AUC: `0.82528` (Δ = `+0.00199`) → **✅ ACCEPT**
- Dropped `ReferralSource_TV`. Remaining features: 55.
- New best params: `{"depth": 5, "learning_rate": 0.081565, "l2_leaf_reg": 5.41842, "bagging_temperature": 0.807314, "random_strength": 0.522818, "border_count": 185, "min_data_in_leaf": 72}`

## Round 5 (features: 55, current score: 0.82528)

**10 least-important features this round (re-ranked from current model):**

```
                 feature  importance
    BookingChannel_Phone    0.000000
ReferralSource_Newspaper    0.000000
 ReferralSource_Magazine    0.000000
  BookingChannel_Website    0.000000
       RoomFloor_Unknown    0.000000
   ReferralSource_Google    0.000000
ReferralSource_Pinterest    0.010603
    ReferralSource_Radio    0.012808
 ReferralSource_LinkedIn    0.017861
              SharedRoom    0.025996
```

### Round 5 — try removing `BookingChannel_Phone`
- New CV ROC-AUC: `0.82401` (Δ = `-0.00127`) → **❌ REJECT**
- Kept `BookingChannel_Phone`. Trying next column.

### Round 5 — try removing `ReferralSource_Newspaper`
- New CV ROC-AUC: `0.82200` (Δ = `-0.00329`) → **❌ REJECT**
- Kept `ReferralSource_Newspaper`. Trying next column.

### Round 5 — try removing `ReferralSource_Magazine`
- New CV ROC-AUC: `0.82100` (Δ = `-0.00428`) → **❌ REJECT**
- Kept `ReferralSource_Magazine`. Trying next column.

### Round 5 — try removing `BookingChannel_Website`
- New CV ROC-AUC: `0.82184` (Δ = `-0.00345`) → **❌ REJECT**
- Kept `BookingChannel_Website`. Trying next column.

### Round 5 — try removing `RoomFloor_Unknown`
- New CV ROC-AUC: `0.82257` (Δ = `-0.00271`) → **❌ REJECT**
- Kept `RoomFloor_Unknown`. Trying next column.

### Round 5 — try removing `ReferralSource_Google`
- New CV ROC-AUC: `0.82259` (Δ = `-0.00270`) → **❌ REJECT**
- Kept `ReferralSource_Google`. Trying next column.

### Round 5 — try removing `ReferralSource_Pinterest`
- New CV ROC-AUC: `0.82371` (Δ = `-0.00157`) → **❌ REJECT**
- Kept `ReferralSource_Pinterest`. Trying next column.

### Round 5 — try removing `ReferralSource_Radio`
- New CV ROC-AUC: `0.82184` (Δ = `-0.00344`) → **❌ REJECT**
- Kept `ReferralSource_Radio`. Trying next column.

### Round 5 — try removing `ReferralSource_LinkedIn`
- New CV ROC-AUC: `0.82112` (Δ = `-0.00416`) → **❌ REJECT**
- Kept `ReferralSource_LinkedIn`. Trying next column.

### Round 5 — try removing `SharedRoom`
- New CV ROC-AUC: `0.82354` (Δ = `-0.00175`) → **❌ REJECT**
- Kept `SharedRoom`. Trying next column.

### Round 5 — try removing `AgeGroup_Unknown`
- New CV ROC-AUC: `0.82501` (Δ = `-0.00028`) → **❌ REJECT**
- Kept `AgeGroup_Unknown`. Trying next column.

### Round 5 — try removing `AgeGroup_Senior`
- New CV ROC-AUC: `0.82283` (Δ = `-0.00245`) → **❌ REJECT**
- Kept `AgeGroup_Senior`. Trying next column.

### Round 5 — try removing `BookingChannel_Mobile`
- New CV ROC-AUC: `0.82430` (Δ = `-0.00098`) → **❌ REJECT**
- Kept `BookingChannel_Mobile`. Trying next column.

### Round 5 — try removing `AgeGroup_Young`
- New CV ROC-AUC: `0.82382` (Δ = `-0.00146`) → **❌ REJECT**
- Kept `AgeGroup_Young`. Trying next column.

### Round 5 — try removing `ReferralSource_Instagram`
- New CV ROC-AUC: `0.82328` (Δ = `-0.00200`) → **❌ REJECT**
- Kept `ReferralSource_Instagram`. Trying next column.

### Round 5 — try removing `ReferralSource_Flyer`
- New CV ROC-AUC: `0.82240` (Δ = `-0.00289`) → **❌ REJECT**
- Kept `ReferralSource_Flyer`. Trying next column.

### Round 5 — try removing `ReferralSource_Facebook`
- New CV ROC-AUC: `0.82356` (Δ = `-0.00172`) → **❌ REJECT**
- Kept `ReferralSource_Facebook`. Trying next column.

### Round 5 — try removing `PackageType_NoPackage`
- New CV ROC-AUC: `0.82212` (Δ = `-0.00316`) → **❌ REJECT**
- Kept `PackageType_NoPackage`. Trying next column.

### Round 5 — try removing `Region_Unknown`
- New CV ROC-AUC: `0.82286` (Δ = `-0.00242`) → **❌ REJECT**
- Kept `Region_Unknown`. Trying next column.

### Round 5 — try removing `VIP`
- New CV ROC-AUC: `0.82471` (Δ = `-0.00058`) → **❌ REJECT**
- Kept `VIP`. Trying next column.

### Round 5 — try removing `ReferralSource_Twitter`
- New CV ROC-AUC: `0.82241` (Δ = `-0.00288`) → **❌ REJECT**
- Kept `ReferralSource_Twitter`. Trying next column.

### Round 5 — try removing `BookingYear`
- New CV ROC-AUC: `0.82141` (Δ = `-0.00387`) → **❌ REJECT**
- Kept `BookingYear`. Trying next column.

### Round 5 — try removing `AgeGroup_Middle`
- New CV ROC-AUC: `0.82314` (Δ = `-0.00214`) → **❌ REJECT**
- Kept `AgeGroup_Middle`. Trying next column.

### Round 5 — try removing `ReferralSource_Podcast`
- New CV ROC-AUC: `0.82800` (Δ = `+0.00272`) → **✅ ACCEPT**
- Dropped `ReferralSource_Podcast`. Remaining features: 54.
- New best params: `{"depth": 5, "learning_rate": 0.285108, "l2_leaf_reg": 4.407069, "bagging_temperature": 0.834396, "random_strength": 2.034641, "border_count": 124, "min_data_in_leaf": 69}`

## Round 6 (features: 54, current score: 0.82800)

**10 least-important features this round (re-ranked from current model):**

```
                 feature  importance
              SharedRoom    0.000000
    BookingChannel_Phone    0.000000
ReferralSource_Pinterest    0.000000
ReferralSource_Newspaper    0.000000
 ReferralSource_LinkedIn    0.000000
   ReferralSource_Google    0.000000
 ReferralSource_Magazine    0.004365
    ReferralSource_Flyer    0.031656
    ReferralSource_Radio    0.040024
          Region_Unknown    0.042754
```

### Round 6 — try removing `SharedRoom`
- New CV ROC-AUC: `0.82242` (Δ = `-0.00558`) → **❌ REJECT**
- Kept `SharedRoom`. Trying next column.

### Round 6 — try removing `BookingChannel_Phone`
- New CV ROC-AUC: `0.82386` (Δ = `-0.00414`) → **❌ REJECT**
- Kept `BookingChannel_Phone`. Trying next column.

### Round 6 — try removing `ReferralSource_Pinterest`
- New CV ROC-AUC: `0.82199` (Δ = `-0.00602`) → **❌ REJECT**
- Kept `ReferralSource_Pinterest`. Trying next column.

### Round 6 — try removing `ReferralSource_Newspaper`
- New CV ROC-AUC: `0.82154` (Δ = `-0.00646`) → **❌ REJECT**
- Kept `ReferralSource_Newspaper`. Trying next column.

### Round 6 — try removing `ReferralSource_LinkedIn`
- New CV ROC-AUC: `0.82285` (Δ = `-0.00515`) → **❌ REJECT**
- Kept `ReferralSource_LinkedIn`. Trying next column.

### Round 6 — try removing `ReferralSource_Google`
- New CV ROC-AUC: `0.82156` (Δ = `-0.00644`) → **❌ REJECT**
- Kept `ReferralSource_Google`. Trying next column.

### Round 6 — try removing `ReferralSource_Magazine`
- New CV ROC-AUC: `0.82228` (Δ = `-0.00572`) → **❌ REJECT**
- Kept `ReferralSource_Magazine`. Trying next column.

### Round 6 — try removing `ReferralSource_Flyer`
- New CV ROC-AUC: `0.82313` (Δ = `-0.00488`) → **❌ REJECT**
- Kept `ReferralSource_Flyer`. Trying next column.

### Round 6 — try removing `ReferralSource_Radio`
- New CV ROC-AUC: `0.82097` (Δ = `-0.00703`) → **❌ REJECT**
- Kept `ReferralSource_Radio`. Trying next column.

### Round 6 — try removing `Region_Unknown`
- New CV ROC-AUC: `0.82271` (Δ = `-0.00530`) → **❌ REJECT**
- Kept `Region_Unknown`. Trying next column.

### Round 6 — try removing `AgeGroup_Unknown`
- New CV ROC-AUC: `0.82328` (Δ = `-0.00472`) → **❌ REJECT**
- Kept `AgeGroup_Unknown`. Trying next column.

### Round 6 — try removing `PackageType_NoPackage`
- New CV ROC-AUC: `0.82400` (Δ = `-0.00400`) → **❌ REJECT**
- Kept `PackageType_NoPackage`. Trying next column.

### Round 6 — try removing `BookingChannel_Mobile`
- New CV ROC-AUC: `0.82340` (Δ = `-0.00460`) → **❌ REJECT**
- Kept `BookingChannel_Mobile`. Trying next column.

### Round 6 — try removing `AgeGroup_Senior`
- New CV ROC-AUC: `0.82328` (Δ = `-0.00473`) → **❌ REJECT**
- Kept `AgeGroup_Senior`. Trying next column.

### Round 6 — try removing `ReferralSource_Facebook`
- New CV ROC-AUC: `0.82199` (Δ = `-0.00601`) → **❌ REJECT**
- Kept `ReferralSource_Facebook`. Trying next column.

### Round 6 — try removing `AgeGroup_Young`
- New CV ROC-AUC: `0.82458` (Δ = `-0.00342`) → **❌ REJECT**
- Kept `AgeGroup_Young`. Trying next column.

### Round 6 — try removing `VIP`
- New CV ROC-AUC: `0.82342` (Δ = `-0.00458`) → **❌ REJECT**
- Kept `VIP`. Trying next column.

### Round 6 — try removing `ReferralSource_Instagram`
- New CV ROC-AUC: `0.82342` (Δ = `-0.00458`) → **❌ REJECT**
- Kept `ReferralSource_Instagram`. Trying next column.

### Round 6 — try removing `ReferralSource_Twitter`
- New CV ROC-AUC: `0.82228` (Δ = `-0.00572`) → **❌ REJECT**
- Kept `ReferralSource_Twitter`. Trying next column.

### Round 6 — try removing `BookingChannel_TravelAgent`
- New CV ROC-AUC: `0.82100` (Δ = `-0.00700`) → **❌ REJECT**
- Kept `BookingChannel_TravelAgent`. Trying next column.

### Round 6 — try removing `PackageType_Wellness`
- New CV ROC-AUC: `0.82199` (Δ = `-0.00601`) → **❌ REJECT**
- Kept `PackageType_Wellness`. Trying next column.

### Round 6 — try removing `RoomFloor_B`
- New CV ROC-AUC: `0.82271` (Δ = `-0.00530`) → **❌ REJECT**
- Kept `RoomFloor_B`. Trying next column.

### Round 6 — try removing `BookingChannel_Website`
- New CV ROC-AUC: `0.82186` (Δ = `-0.00614`) → **❌ REJECT**
- Kept `BookingChannel_Website`. Trying next column.

### Round 6 — try removing `AgeGroup_Middle`
- New CV ROC-AUC: `0.82299` (Δ = `-0.00502`) → **❌ REJECT**
- Kept `AgeGroup_Middle`. Trying next column.

### Round 6 — try removing `PackageType_Relaxation`
- New CV ROC-AUC: `0.81937` (Δ = `-0.00864`) → **❌ REJECT**
- Kept `PackageType_Relaxation`. Trying next column.

### Round 6 — try removing `BookingYear`
- New CV ROC-AUC: `0.82255` (Δ = `-0.00546`) → **❌ REJECT**
- Kept `BookingYear`. Trying next column.

### Round 6 — try removing `SurveyScore`
- New CV ROC-AUC: `0.82156` (Δ = `-0.00644`) → **❌ REJECT**
- Kept `SurveyScore`. Trying next column.

### Round 6 — try removing `ReferralSource_YouTube`
- New CV ROC-AUC: `0.82215` (Δ = `-0.00585`) → **❌ REJECT**
- Kept `ReferralSource_YouTube`. Trying next column.

### Round 6 — try removing `ReferralSource_Yelp`
- New CV ROC-AUC: `0.81984` (Δ = `-0.00816`) → **❌ REJECT**
- Kept `ReferralSource_Yelp`. Trying next column.

### Round 6 — try removing `RoomFloor_Unknown`
- New CV ROC-AUC: `0.82228` (Δ = `-0.00572`) → **❌ REJECT**
- Kept `RoomFloor_Unknown`. Trying next column.

### Round 6 — try removing `DaysSinceEmail`
- New CV ROC-AUC: `0.82157` (Δ = `-0.00644`) → **❌ REJECT**
- Kept `DaysSinceEmail`. Trying next column.

### Round 6 — try removing `ReferralSource_TripAdvisor`
- New CV ROC-AUC: `0.81852` (Δ = `-0.00948`) → **❌ REJECT**
- Kept `ReferralSource_TripAdvisor`. Trying next column.

### Round 6 — try removing `RoomFloor_E`
- New CV ROC-AUC: `0.82313` (Δ = `-0.00487`) → **❌ REJECT**
- Kept `RoomFloor_E`. Trying next column.

### Round 6 — try removing `BookingMonth`
- New CV ROC-AUC: `0.82099` (Δ = `-0.00701`) → **❌ REJECT**
- Kept `BookingMonth`. Trying next column.

### Round 6 — try removing `LoyaltyPoints`
- New CV ROC-AUC: `0.82055` (Δ = `-0.00745`) → **❌ REJECT**
- Kept `LoyaltyPoints`. Trying next column.

### Round 6 — try removing `ReferralSource_Email`
- New CV ROC-AUC: `0.81828` (Δ = `-0.00972`) → **❌ REJECT**
- Kept `ReferralSource_Email`. Trying next column.

### Round 6 — try removing `RoomFloor_C`
- New CV ROC-AUC: `0.82108` (Δ = `-0.00692`) → **❌ REJECT**
- Kept `RoomFloor_C`. Trying next column.

### Round 6 — try removing `AgeGroup_Minor`
- New CV ROC-AUC: `0.82097` (Δ = `-0.00703`) → **❌ REJECT**
- Kept `AgeGroup_Minor`. Trying next column.

### Round 6 — try removing `Retail`
- New CV ROC-AUC: `0.81591` (Δ = `-0.01209`) → **❌ REJECT**
- Kept `Retail`. Trying next column.

### Round 6 — try removing `ReferralSource_TikTok`
- New CV ROC-AUC: `0.82155` (Δ = `-0.00645`) → **❌ REJECT**
- Kept `ReferralSource_TikTok`. Trying next column.

### Round 6 — try removing `RoomService`
- New CV ROC-AUC: `0.81425` (Δ = `-0.01375`) → **❌ REJECT**
- Kept `RoomService`. Trying next column.

### Round 6 — try removing `Dining`
- New CV ROC-AUC: `0.81683` (Δ = `-0.01117`) → **❌ REJECT**
- Kept `Dining`. Trying next column.

### Round 6 — try removing `Region_AsiaPacific`
- New CV ROC-AUC: `0.82009` (Δ = `-0.00791`) → **❌ REJECT**
- Kept `Region_AsiaPacific`. Trying next column.

### Round 6 — try removing `ReferralSource_Friend`
- New CV ROC-AUC: `0.81743` (Δ = `-0.01057`) → **❌ REJECT**
- Kept `ReferralSource_Friend`. Trying next column.

### Round 6 — try removing `RoomFloor_F`
- New CV ROC-AUC: `0.82096` (Δ = `-0.00704`) → **❌ REJECT**
- Kept `RoomFloor_F`. Trying next column.

### Round 6 — try removing `RoomSide_S`
- New CV ROC-AUC: `0.81305` (Δ = `-0.01495`) → **❌ REJECT**
- Kept `RoomSide_S`. Trying next column.

### Round 6 — try removing `PromoCode_PromoA`
- New CV ROC-AUC: `0.81100` (Δ = `-0.01700`) → **❌ REJECT**
- Kept `PromoCode_PromoA`. Trying next column.

### Round 6 — try removing `RoomFloor_G`
- New CV ROC-AUC: `0.82254` (Δ = `-0.00546`) → **❌ REJECT**
- Kept `RoomFloor_G`. Trying next column.

### Round 6 — try removing `PromoCode_PromoB`
- New CV ROC-AUC: `0.81496` (Δ = `-0.01304`) → **❌ REJECT**
- Kept `PromoCode_PromoB`. Trying next column.

### Round 6 — try removing `Entertainment`
- New CV ROC-AUC: `0.81193` (Δ = `-0.01608`) → **❌ REJECT**
- Kept `Entertainment`. Trying next column.

### Round 6 — try removing `RoomNumber`
- New CV ROC-AUC: `0.81577` (Δ = `-0.01223`) → **❌ REJECT**
- Kept `RoomNumber`. Trying next column.

### Round 6 — try removing `Region_Europe`
- New CV ROC-AUC: `0.82154` (Δ = `-0.00647`) → **❌ REJECT**
- Kept `Region_Europe`. Trying next column.

### Round 6 — try removing `Spa`
- New CV ROC-AUC: `0.80936` (Δ = `-0.01864`) → **❌ REJECT**
- Kept `Spa`. Trying next column.

### Round 6 — try removing `AllInclusive`
- New CV ROC-AUC: `0.79959` (Δ = `-0.02842`) → **❌ REJECT**
- Kept `AllInclusive`. Trying next column.

## Stop — round 6 produced no improvement > 0.0.

## Search summary

- **Final CV ROC-AUC (during search):** `0.82800` (baseline `0.82114`, Δ = `+0.00686`)
- Removed 5 columns in order: `['RoomFloor_T', 'RoomFloor_D', 'RoomSide_Unknown', 'ReferralSource_TV', 'ReferralSource_Podcast']`
- Kept 54 columns: `['AllInclusive', 'VIP', 'RoomService', 'Dining', 'Retail', 'Spa', 'Entertainment', 'LoyaltyPoints', 'SurveyScore', 'DaysSinceEmail', 'SharedRoom', 'RoomNumber', 'BookingMonth', 'BookingYear', 'PromoCode_PromoA', 'PromoCode_PromoB', 'Region_AsiaPacific', 'Region_Europe', 'Region_Unknown', 'PackageType_NoPackage', 'PackageType_Relaxation', 'PackageType_Wellness', 'AgeGroup_Middle', 'AgeGroup_Minor', 'AgeGroup_Senior', 'AgeGroup_Unknown', 'AgeGroup_Young', 'RoomFloor_B', 'RoomFloor_C', 'RoomFloor_E', 'RoomFloor_F', 'RoomFloor_G', 'RoomFloor_Unknown', 'RoomSide_S', 'BookingChannel_Mobile', 'BookingChannel_Phone', 'BookingChannel_TravelAgent', 'BookingChannel_Website', 'ReferralSource_Email', 'ReferralSource_Facebook', 'ReferralSource_Flyer', 'ReferralSource_Friend', 'ReferralSource_Google', 'ReferralSource_Instagram', 'ReferralSource_LinkedIn', 'ReferralSource_Magazine', 'ReferralSource_Newspaper', 'ReferralSource_Pinterest', 'ReferralSource_Radio', 'ReferralSource_TikTok', 'ReferralSource_TripAdvisor', 'ReferralSource_Twitter', 'ReferralSource_Yelp', 'ReferralSource_YouTube']`

## Final re-tune (50 trials on winning feature set)

- Re-tuned CV ROC-AUC: `0.82800` (search result was `0.82800`)
- Re-tuned best params: `{"depth": 5, "learning_rate": 0.285108, "l2_leaf_reg": 4.407069, "bagging_temperature": 0.834396, "random_strength": 2.034641, "border_count": 124, "min_data_in_leaf": 69}`

ℹ️ Re-tune did not beat the search result — falling back to search-result params for the submission.

- **Winning features (54):** `['AllInclusive', 'VIP', 'RoomService', 'Dining', 'Retail', 'Spa', 'Entertainment', 'LoyaltyPoints', 'SurveyScore', 'DaysSinceEmail', 'SharedRoom', 'RoomNumber', 'BookingMonth', 'BookingYear', 'PromoCode_PromoA', 'PromoCode_PromoB', 'Region_AsiaPacific', 'Region_Europe', 'Region_Unknown', 'PackageType_NoPackage', 'PackageType_Relaxation', 'PackageType_Wellness', 'AgeGroup_Middle', 'AgeGroup_Minor', 'AgeGroup_Senior', 'AgeGroup_Unknown', 'AgeGroup_Young', 'RoomFloor_B', 'RoomFloor_C', 'RoomFloor_E', 'RoomFloor_F', 'RoomFloor_G', 'RoomFloor_Unknown', 'RoomSide_S', 'BookingChannel_Mobile', 'BookingChannel_Phone', 'BookingChannel_TravelAgent', 'BookingChannel_Website', 'ReferralSource_Email', 'ReferralSource_Facebook', 'ReferralSource_Flyer', 'ReferralSource_Friend', 'ReferralSource_Google', 'ReferralSource_Instagram', 'ReferralSource_LinkedIn', 'ReferralSource_Magazine', 'ReferralSource_Newspaper', 'ReferralSource_Pinterest', 'ReferralSource_Radio', 'ReferralSource_TikTok', 'ReferralSource_TripAdvisor', 'ReferralSource_Twitter', 'ReferralSource_Yelp', 'ReferralSource_YouTube']`
- **Winning CV ROC-AUC:** `0.82800`
- **Winning params:** `{"depth": 5, "learning_rate": 0.285108, "l2_leaf_reg": 4.407069, "bagging_temperature": 0.834396, "random_strength": 2.034641, "border_count": 124, "min_data_in_leaf": 69}`

## Submission

- Wrote `submission.csv` (1739 rows)
- Predictions: 829 True, 910 False

**Completed:** 2026-05-24T11:53:52

