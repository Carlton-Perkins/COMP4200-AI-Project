[IN PROGRESS]

Stats: 2689 craftsmanship / 2872 control / 572 cp

Crafting system equations: https://docs.google.com/document/d/1Da48dDVPB7N4ignxGeo0UeJ_6R0kQRqzLUH-TkpSQRc/edit

Expert craft rarity values (make copy, unhide data): https://docs.google.com/spreadsheets/d/1sxIiFIDW0D7UcNjn8kD_Vt6GzwI39CYg4K6415JrrIA/edit#gid=1475917965

Recipe difficulty (progress goal): 11126

Recipe quality cap: 82400

Recipe durability: 50

Recipe level: 511

5800 collectability -> 175 skyward pts

Lowest tier equation: score = ? * (collectability - 5800) + 175 for 5800 <= x <= 6499

Mid tier equation: 0.45 * (collectability - 6500) + 370 for 6500 <= x <= 7699

Max tier equation: 0.3 * (collectability - 7700) + 1100 for 7700 <= x <= 8240

Crafting Actions
| Name | Progress Efficiency | Quality Efficiency | Success Rate | Notes | CP Cost |
|------|---------------------|--------------------|--------------|-------|---------|
| Basic Synthesis | 120% | 0% | 100% | N/A | 0 |
| Rapid Synthesis | 500% | 0% | 50% | N/A | 0 |
| Careful Synthesis | 150% | 0% | 100% | N/A | 7 |
| Groundwork | 300% | 0% | 100% | Durability cost is 20 instead of 10. Efficiency is 150% if current durability < cost. | 18 |
| Intensive Synthesis | 300% | 0% | 100% | Can only be used when material condition is Good | 6 |
| Muscle Memory | 300% | 0% | 100% | Can only be used on first turn. Increases efficiency of next synthesis by 100% (lasts 5 turns) | 6 |
| Name of the Elements | 0% | 0% | 100% | For next 3 steps, efficiency of Brand of the Elements is increased by up to 200% dependent on current progress | 30 |
| Brand of the Elements | 100% | 0% | 100% | N/A | 6 |
| Veneration | 0% | 0% | 100% | Increases synthesis action efficiency by 50% for next 4 steps | 18 |
| Final Appraisal | 0% | 0% | 100% | Next synthesis action that would complete craft leaves 1 progress remaining (lasts for 5 steps) | 1 |
| Delicate Synthesis | 100% | 100% | 100% | N/A | 32 |
| Basic Touch | 0% | 100% | 100% | N/A | 18 |
| Hasty Touch | 0% | 100% | 60% | N/A | 0 |
| Standard Touch | 0% | 125% | 100% | N/A | 32 |
| Preparatory Touch | 0% | 200% | 100% | Gives an extra IQ stack. Durability cost is 20 instead of 10 | 40 |
| Precise Touch | 0% | 150% | 100% | Gives an extra IQ stack. Can only be used when material condition is Good | 18 |
| Patient Touch | 0% | 100% | 50% | Doubles IQ stacks if successful, halves them if it fails | 6 |
| Prudent Touch | 0% | 100% | 100% | Increases quality for half durability cost (not usable when either Waste Not buff is active) | 25 |
| Reflect | 0% | 100% | 100% | Can only be used on first turn. Grants 3 IQ stacks | 24 |
| Byregot's Blessing | 0% | 100%+ (see buff) | 100% | Gains 20% quality efficiency for each IQ stack (additive); consumes stacks | 24 |
| Great Strides | 0% | 0% | 100% | Increases next Touch action (lasts 3 steps) | 32 |
| Innovation | 0% | 0% | 100% | Increases Touch action efficiency by 50% for next 4 steps | 18 |
| Inner Quiet | 0% | 0% | 100% | Grants bonus to control (quality stat) with every increase in quality (see crafting equations) (max 11 stacks) | 18 |
| Observe | 0% | 0% | 100% | Does nothing for one step | 7 |
| Focused Synthesis | 200% | 0% | 50% | Accuracy increased to 100% if used directly after Observe | 5 |
| Focused Touch | 0% | 150% | 50% | Accuracy increased to 100% if used directly after Observe | 18 |
| Tricks of the Trade | 0% | 0% | 100% | Restores CP by 20. Can only be used when material condition is Good | 0 |
| Waste Not | 0% | 0% | 100% | Cuts durability loss in half for the next 4 steps | 56 |
| Waste Not II | 0% | 0% | 100% | Cuts durability loss in half for the next 8 steps | 98 |
| Master's Mend | 0% | 0% | 100% | Restores durability by 30 (cannot overcap) | 88 |
| Manipulation | 0% | 0% | 100% | Restores 5 durability after each step for the next 8 steps | 96 |

Notes:
- Did not include Trained Eye. It is not possible to use on expert crafts, as they are level 80.
- Anything that affects "touch" actions also affects Byregot's Blessing and the quality increase on Delicate Synthesis.
    - Need to test whether Delicate Synthesis also increases IQ stacks.
- Anything that can be used on a Good can also be used on an Excellent, but Excellent and Poor procs do not exist in expert crafts.
- Base durability cost is 10.
