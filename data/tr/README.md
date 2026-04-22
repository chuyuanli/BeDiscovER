## Dataset source

Licensing note: redistributed data files in this repository for the `tr` task
should be treated under **CC BY 4.0**. Individual source datasets remain
subject to their original upstream notices.

- TimeBank-Dense:
  - paper: https://aclanthology.org/P14-2082.pdf
  - github: https://github.com/muk343/TimeBank-dense
  - data: https://www.usna.edu/Users/cs/nchamber/caevo/#corpus
  - license: we follow its original copyright text and acknowledgements of developers, see [LICENSE](TBD_LICENSE.md).
- TDDiscourse
    - paper: https://aclanthology.org/W19-5929.pdf
    - github: https://github.com/aakanksha19/TDDiscourse
    - license: CC-BY-4.0
- Test of Time (arithmetic part): ToT-arith
    - paper: https://openreview.net/pdf?id=44CoQe6VCq
    - license: CC-BY-4.0


## Data sizes 
- TB-Dense: 
  - only event-event relations (`tbd-ee`), in total 1515 relation pairs
  - 6 relations: IS_INCLUDED, INCLUDES, SIMULTANEOUS, BEFORE, AFTER, NONE
  - percentage: 
      ```
      Before	390	0.257
      Includes	68	0.045
      Is_included	76	0.050
      SIMULTANEOUS	48	0.032
      After	291	0.192
      None	642	0.424
      ```

- TDD-Man
  - 5 relations: after, before, simultaneous, includes, is_included
  - percentage: 0.13 0.27 0.03 0.38 0.19
  
