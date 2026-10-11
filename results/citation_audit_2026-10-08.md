# Citation audit: star.bib, 23 cited keys (TACAS 2027 submission)

Date: 2026-10-08. Every claim below was checked against the source named in the table; nothing is from memory. Sources used: Crossref registry records (publisher-deposited metadata, fetched from api.crossref.org/works/<doi>), the DOI resolver, EasyChair volume pages reached by resolving the EPiC DOIs, Springer chapter pages (link.springer.com), the NeurIPS proceedings site, the arXiv API, Open Library, and the Internet Archive capture of the NASA post. DBLP, the ACM DL, AIAA, and mitpress.mit.edu refused automated fetches during this session; where that left a field unverified the table says so.

Verdict key: CONFIRMED = exists and the present fields are right (entry may still be incomplete); EXISTS-BUT-METADATA-WRONG = the work exists but one or more present fields are wrong; NOT-FOUND = no work with the stated title, authors, venue and DOI together exists; UNVERIFIABLE = could not be checked against a primary source.

## (a) Summary table

| key | verdict | what is wrong / missing | source URL |
|---|---|---|---|
| 2016cora | EXISTS-BUT-METADATA-WRONG (not a citable publication) | "CORA 2016 manual" is an unpublished tool manual; journal=TU Munich, volume=85748 (the Garching postal code), publisher=Citeseer are not bibliographic data. Replace with the ARCH 2015 paper: Althoff, "An Introduction to CORA 2015", ARCH14-15, EPiC Series in Computing 34, pp. 120-151, EasyChair, DOI 10.29007/zbkv, 2015. Kochdumper is not an author of that paper. | https://doi.org/10.29007/zbkv (resolves to https://easychair.org/publications/paper/xMm) |
| 2019juliareach | CONFIRMED | Title, authors, venue, pages 39-44, 2019 all match. Missing DOI 10.1145/3302504.3311804, publisher ACM, location Montreal. | https://api.crossref.org/works/10.1145/3302504.3311804 |
| 2020arch | CONFIRMED (author list truncated) | Title, pages 49-75, 2020 match. Author list ends in "and others" (13 authors in the published record). Missing series EPiC Series in Computing, volume 74, publisher EasyChair, DOI 10.29007/zkf6, editors. | https://doi.org/10.29007/zkf6 (https://easychair.org/publications/paper/nrdD) |
| 2024archNL | EXISTS-BUT-METADATA-WRONG | Author list is wrong: the published list is Geretti, Alexandre Dit Sandretto, Althoff, Benet, Collins, Forets, Mitsch, Schilling, Tillet, Wetzlinger (10). The entry names Chapoutot, Kim, Linares and Sanders, who are not authors, and omits Mitsch and Tillet. Missing volume 103, pages 39-63, publisher EasyChair, DOI 10.29007/21ch. | https://doi.org/10.29007/21ch (https://easychair.org/publications/paper/QD5d) |
| AlthoffFrehseGirard2021 | CONFIRMED | All fields match. Issue number 1 and publisher Annual Reviews can be added. | https://api.crossref.org/works/10.1146/annurev-control-071420-081941 |
| ChanM17CDC | CONFIRMED (incomplete) | Exists as stated. Missing pages 1427-1432, DOI 10.1109/CDC.2017.8263854, publisher IEEE, location Melbourne. Official title of the proceedings: "2017 IEEE 56th Annual Conference on Decision and Control (CDC)". | https://api.crossref.org/works/10.1109/CDC.2017.8263854 |
| ChenSankaranarayanan2022 | CONFIRMED | DOI resolves to this chapter; LNCS 13260, pp. 109-130, Springer. Editors (Deshmukh, Havelund, Perez) can be added. | https://link.springer.com/chapter/10.1007/978-3-031-06773-0_6 |
| FloresAbad2014 | CONFIRMED | DOI resolves to this article; vol. 68, pp. 1-26, 2014. Publisher Elsevier can be added. | https://api.crossref.org/works/10.1016/j.paerosci.2014.03.002 |
| Hobbs2020 | NOT-FOUND (composite of three different works) | DOI 10.2514/6.2020-0132 resolves to Orme, Soderquist, Gorrell, "Analysis of Distortion Phase Shift in a Highly Loaded Fan Stage", AIAA Scitech 2020 Forum. The title "Assured Autonomy: Path Toward Living With Autonomous Systems We Can Trust" belongs to a CCC workshop report by Topcu, Bliss, Cooke, Cummings, Llorens, Shrobe, Zuck (arXiv:2010.14443, Oct 2020), not to Hobbs et al. The author list Hobbs, Mote, Abate, Coogan, Feron belongs to "Runtime Assurance for Safety-Critical Systems: An Introduction to Safety Filtering Approaches for Complex Control Systems", IEEE Control Systems (the Control Systems Magazine, ISSN 1066-033X) 43(2):28-65, April 2023, DOI 10.1109/MCS.2023.3234380. No paper with this title and this author list exists. Replacement entries for all three real works are given below; the three \cite sites (sec-intro.tex:25, sec-related.tex:23, sec-satellite.tex:10) must be re-pointed by the authors to whichever work they actually read. | https://api.crossref.org/works/10.2514/6.2020-0132 ; http://export.arxiv.org/api/query?id_list=2010.14443 ; https://api.crossref.org/works/10.1109/mcs.2023.3234380 |
| JGMDE:satellite2012 | CONFIRMED (incomplete) | Exists; pp. 252-266, 2012. Missing DOI 10.1007/978-3-642-32759-9_22, series LNCS vol. 7436, publisher Springer, editors Giannakopoulou and Méry; booktitle should name the volume "FM 2012: Formal Methods". Springer prints the fifth author as "Richard Scott Erwin" (R. Scott Erwin is the form he uses; either is fine). | https://link.springer.com/chapter/10.1007/978-3-642-32759-9_22 |
| Kessler1978 | CONFIRMED | DOI resolves to this article; vol. 83, no. A6, pp. 2637-2646, June 1978. The 1978 masthead read "Journal of Geophysical Research"; AGU's deposited record uses "Journal of Geophysical Research: Space Physics". Both acceptable. | https://api.crossref.org/works/10.1029/JA083iA06p02637 |
| Mitra2021CPS | CONFIRMED | Publisher MIT Press, 2021, ISBN 9780262044806, 304 pp. confirmed from the Open Library catalog record (mitpress.mit.edu refused automated fetches; the MIT Press Bookstore listing agrees and places it in the MIT Press "Cyber Physical Systems Series"). Add address Cambridge, MA. | https://openlibrary.org/isbn/9780262044806.json |
| dryvr | CONFIRMED (CoRR version; CAV version preferred) | arXiv:1702.06902 exists with these authors and title. The field `title = {{DRYVR:} ...}` forces the all-caps "DRYVR" into print; the published title is "DryVR". The peer-reviewed version is CAV 2017, LNCS 10426, pp. 441-461, DOI 10.1007/978-3-319-63387-9_22, Springer; both entries are given below. | http://export.arxiv.org/api/query?id_list=1702.06902 ; https://link.springer.com/chapter/10.1007/978-3-319-63387-9_22 |
| dunlap2023rta | CONFIRMED (one author spelling UNVERIFIABLE) | DOI 10.2514/1.I011126 resolves to this article; J. Aerosp. Inf. Syst. 20(1):25-36, Jan 2023. AIAA's deposited record for the journal article lists the third author as "Kaiden Delsing"; AIAA's record for the SciTech 2022 conference version (DOI 10.2514/6.2022-1853) lists "Kai Delsing". The AIAA page itself could not be fetched, so the printed form is unverified; check the journal PDF. | https://api.crossref.org/works/10.2514/1.I011126 |
| erwin-cdc16 | CONFIRMED (incomplete) | Exists; first author's surname is spelled "Jewison" (Christopher Jewison), as in the entry. Missing pages 3300-3305, DOI 10.1109/CDC.2016.7798765, publisher IEEE. Official proceedings title: "2016 IEEE 55th Conference on Decision and Control (CDC)". | https://api.crossref.org/works/10.1109/cdc.2016.7798765 |
| li2023verse | CONFIRMED (incomplete) | Exists; pp. 351-364, 2023. Missing DOI 10.1007/978-3-031-37706-8_18, series LNCS vol. 13964, publisher Springer, editors Enea and Lal; booktitle should name the volume "Computer Aided Verification (CAV 2023)". | https://link.springer.com/chapter/10.1007/978-3-031-37706-8_18 |
| miller2024satellite | CONFIRMED | Pages 2298-2303 confirmed. Missing DOI 10.23919/ACC60939.2024.10644961, publisher IEEE, location Toronto. | https://api.crossref.org/works/10.23919/acc60939.2024.10644961 |
| rdvzvis | CONFIRMED (entry malformed) | DOI resolves to this paper; pp. 1803-1808, CDC 2008, Cancun. The author field `LaValle, \{Steven M.\}` contains escaped braces, which BibTeX prints literally; the abstract, language, isbn, note and address fields are clutter. Clean entry below. | https://api.crossref.org/works/10.1109/CDC.2008.4739343 |
| scipy_2020 | CONFIRMED (author list incomplete; entry malformed) | DOI resolves to this article; Nature Methods 17(3):261-272, 2020. The published byline is the 34 named authors "and SciPy 1.0 Contributors"; the consortium author is missing. Diacritics dropped (Stéfan J. van der Walt, İlhan Polat, Antônio H. Ribeiro). The entry carries a local Zotero `file` path and ends with a stray comma after the closing brace. | https://api.crossref.org/works/10.1038/s41592-019-0686-2 |
| stanleycar | EXISTS-BUT-METADATA-WRONG | DOI resolves to this paper. Missing booktitle "2007 American Control Conference", publisher IEEE, location New York. month=08 is wrong: the conference ran 9-13 July 2007 and the record is dated July 2007. First names: Gabriel M. Hoffmann, Claire J. Tomlin. | https://api.crossref.org/works/10.1109/ACC.2007.4282788 |
| z3 | EXISTS-BUT-METADATA-WRONG | Exists; pp. 337-340, 2008. The booktitle is the ACM DL's garbled string ("Proceedings of the Theory and practice of software, 14th international conference on Tools and algorithms..."). Correct venue: Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2008), LNCS 4963, Springer, eds. Ramakrishnan and Rehof, DOI 10.1007/978-3-540-78800-3_24 (missing). | https://link.springer.com/chapter/10.1007/978-3-540-78800-3_24 |
| zhang2018efficientneuralnetworkrobustness | CONFIRMED (cite the proceedings version) | arXiv:1811.00866 exists with these authors and title. The paper appeared in Advances in Neural Information Processing Systems 31 (NeurIPS 2018), Curran Associates; a reviewer will expect that, not the @misc arXiv form. Page range UNVERIFIABLE: NeurIPS's own BibTeX leaves `pages` empty and DBLP/ACM blocked fetches, so the entry below omits pages. | https://proceedings.neurips.cc/paper/2018/hash/d04863f100d59b3eb688a11f95b0ae60-Abstract.html ; https://proceedings.neurips.cc/paper/2018/file/d04863f100d59b3eb688a11f95b0ae60-Bibtex.bib |
| nasa2020ae | CONFIRMED (URL now dead) | The post "Crew Dragon Exits Station's Approach Ellipsoid" was published on the NASA Commercial Crew Program blog on August 1, 2020 (19:56 EDT), no byline. The cited URL now returns 301 to https://www.nasa.gov/blogs/ and the post is no longer served there; the "Accessed October 2026" note therefore does not describe a page a reader can reach. Internet Archive captures exist (2020-08-07, 2021-03-20, 2025-04-27); the entry below cites the archived copy. | https://web.archive.org/web/20200807001726/https://blogs.nasa.gov/commercialcrew/2020/08/01/crew-dragon-exits-stations-approach-ellipsoid-2/ |

Counts: 3 NOT-FOUND or replaced as a unit (Hobbs2020; 2016cora replaced by the ARCH 2015 paper), 4 EXISTS-BUT-METADATA-WRONG (2024archNL, stanleycar, z3, plus 2016cora), 16 CONFIRMED of which 13 need added fields or cleanup. Two fields remain UNVERIFIABLE (NeurIPS 2018 pages; printed spelling of the Dunlap third author).

## (b) Corrected BibTeX entries

Each entry below is complete (every author in published order, full venue, series/volume/publisher/pages where the venue has them, DOI where one exists) and ready to paste over the existing entry of the same key. Keys are unchanged except where noted.

### 2016cora (replace the manual with the ARCH 2015 paper; keep the key so \cite sites need no change)

```bibtex
@inproceedings{2016cora,
  author    = {Matthias Althoff},
  title     = {An Introduction to {CORA} 2015},
  booktitle = {ARCH14-15. 1st and 2nd International Workshop on Applied veRification for Continuous and Hybrid Systems},
  editor    = {Goran Frehse and Matthias Althoff},
  series    = {EPiC Series in Computing},
  volume    = {34},
  pages     = {120--151},
  publisher = {EasyChair},
  year      = {2015},
  doi       = {10.29007/zbkv}
}
```

### 2019juliareach

```bibtex
@inproceedings{2019juliareach,
  author    = {Sergiy Bogomolov and Marcelo Forets and Goran Frehse and Kostiantyn Potomkin and Christian Schilling},
  title     = {{JuliaReach}: A Toolbox for Set-Based Reachability},
  booktitle = {Proceedings of the 22nd ACM International Conference on Hybrid Systems: Computation and Control (HSCC 2019)},
  pages     = {39--44},
  publisher = {ACM},
  address   = {Montreal, QC, Canada},
  year      = {2019},
  doi       = {10.1145/3302504.3311804}
}
```

### 2020arch

```bibtex
@inproceedings{2020arch,
  author    = {Luca Geretti and Julien {Alexandre Dit Sandretto} and Matthias Althoff and Luis Benet and Alexandre Chapoutot and Xin Chen and Pieter Collins and Marcelo Forets and Daniel Freire and Fabian Immler and Niklas Kochdumper and David P. Sanders and Christian Schilling},
  title     = {{ARCH-COMP20} Category Report: Continuous and Hybrid Systems with Nonlinear Dynamics},
  booktitle = {ARCH20. 7th International Workshop on Applied Verification of Continuous and Hybrid Systems (ARCH20)},
  editor    = {Goran Frehse and Matthias Althoff},
  series    = {EPiC Series in Computing},
  volume    = {74},
  pages     = {49--75},
  publisher = {EasyChair},
  year      = {2020},
  doi       = {10.29007/zkf6}
}
```

### 2024archNL

```bibtex
@inproceedings{2024archNL,
  author    = {Luca Geretti and Julien {Alexandre Dit Sandretto} and Matthias Althoff and Luis Benet and Pieter Collins and Marcelo Forets and Stefan Mitsch and Christian Schilling and Joris Tillet and Mark Wetzlinger},
  title     = {{ARCH-COMP24} Category Report: Continuous and Hybrid Systems with Nonlinear Dynamics},
  booktitle = {Proceedings of the 11th International Workshop on Applied Verification for Continuous and Hybrid Systems (ARCH24)},
  editor    = {Goran Frehse and Matthias Althoff},
  series    = {EPiC Series in Computing},
  volume    = {103},
  pages     = {39--63},
  publisher = {EasyChair},
  year      = {2024},
  doi       = {10.29007/21ch}
}
```

### AlthoffFrehseGirard2021

```bibtex
@article{AlthoffFrehseGirard2021,
  author    = {Matthias Althoff and Goran Frehse and Antoine Girard},
  title     = {Set Propagation Techniques for Reachability Analysis},
  journal   = {Annual Review of Control, Robotics, and Autonomous Systems},
  volume    = {4},
  number    = {1},
  pages     = {369--395},
  publisher = {Annual Reviews},
  year      = {2021},
  doi       = {10.1146/annurev-control-071420-081941}
}
```

### ChanM17CDC

```bibtex
@inproceedings{ChanM17CDC,
  author    = {Nicole Chan and Sayan Mitra},
  title     = {Verified Hybrid {LQ} Control for Autonomous Spacecraft Rendezvous},
  booktitle = {2017 IEEE 56th Annual Conference on Decision and Control (CDC)},
  pages     = {1427--1432},
  publisher = {IEEE},
  address   = {Melbourne, Australia},
  month     = dec,
  year      = {2017},
  doi       = {10.1109/CDC.2017.8263854}
}
```

### ChenSankaranarayanan2022

```bibtex
@inproceedings{ChenSankaranarayanan2022,
  author    = {Xin Chen and Sriram Sankaranarayanan},
  title     = {Reachability Analysis for Cyber-Physical Systems: Are We There Yet?},
  booktitle = {NASA Formal Methods (NFM 2022)},
  editor    = {Jyotirmoy V. Deshmukh and Klaus Havelund and Ivan Perez},
  series    = {Lecture Notes in Computer Science},
  volume    = {13260},
  pages     = {109--130},
  publisher = {Springer},
  address   = {Cham},
  year      = {2022},
  doi       = {10.1007/978-3-031-06773-0_6}
}
```

### FloresAbad2014

```bibtex
@article{FloresAbad2014,
  author    = {Angel Flores-Abad and Ou Ma and Khanh Pham and Steve Ulrich},
  title     = {A Review of Space Robotics Technologies for On-Orbit Servicing},
  journal   = {Progress in Aerospace Sciences},
  volume    = {68},
  pages     = {1--26},
  publisher = {Elsevier},
  year      = {2014},
  doi       = {10.1016/j.paerosci.2014.03.002}
}
```

### Hobbs2020 (delete; choose among the three real works below and re-point the \cite sites)

The CCC workshop report that carries the cited title:

```bibtex
@techreport{Topcu2020AssuredAutonomy,
  author      = {Ufuk Topcu and Nadya Bliss and Nancy Cooke and Missy Cummings and Ashley Llorens and Howard Shrobe and Lenore Zuck},
  title       = {Assured Autonomy: Path Toward Living With Autonomous Systems We Can Trust},
  institution = {Computing Community Consortium (CCC)},
  type        = {Workshop report},
  year        = {2020},
  month       = oct,
  note        = {arXiv:2010.14443},
  url         = {https://arxiv.org/abs/2010.14443}
}
```

The paper by the cited author list (runtime assurance survey, with spacecraft examples):

```bibtex
@article{Hobbs2023RTA,
  author    = {Kerianne L. Hobbs and Mark L. Mote and Matthew C. L. Abate and Samuel D. Coogan and Eric M. Feron},
  title     = {Runtime Assurance for Safety-Critical Systems: An Introduction to Safety Filtering Approaches for Complex Control Systems},
  journal   = {IEEE Control Systems},
  volume    = {43},
  number    = {2},
  pages     = {28--65},
  publisher = {IEEE},
  year      = {2023},
  doi       = {10.1109/MCS.2023.3234380}
}
```

The only Hobbs paper in the AIAA Scitech 2020 Forum (collision-avoidance taxonomy for space traffic management):

```bibtex
@inproceedings{HobbsFeron2020Taxonomy,
  author    = {Kerianne L. Hobbs and Eric M. Feron},
  title     = {A Taxonomy for Aerospace Collision Avoidance with Implications for Automation in Space Traffic Management},
  booktitle = {AIAA Scitech 2020 Forum},
  publisher = {American Institute of Aeronautics and Astronautics},
  address   = {Orlando, FL, USA},
  year      = {2020},
  doi       = {10.2514/6.2020-0877}
}
```

(The address for the Scitech entry is the forum's location as given by AIAA's event record; omit it if not wanted.)

### JGMDE:satellite2012

```bibtex
@inproceedings{JGMDE:satellite2012,
  author    = {Taylor T. Johnson and Jeremy Green and Sayan Mitra and Rachel Dudley and R. Scott Erwin},
  title     = {Satellite Rendezvous and Conjunction Avoidance: Case Studies in Verification of Nonlinear Hybrid Systems},
  booktitle = {FM 2012: Formal Methods},
  editor    = {Dimitra Giannakopoulou and Dominique M{\'e}ry},
  series    = {Lecture Notes in Computer Science},
  volume    = {7436},
  pages     = {252--266},
  publisher = {Springer},
  address   = {Berlin, Heidelberg},
  year      = {2012},
  doi       = {10.1007/978-3-642-32759-9_22}
}
```

### Kessler1978

```bibtex
@article{Kessler1978,
  author    = {Donald J. Kessler and Burton G. Cour-Palais},
  title     = {Collision Frequency of Artificial Satellites: The Creation of a Debris Belt},
  journal   = {Journal of Geophysical Research: Space Physics},
  volume    = {83},
  number    = {A6},
  pages     = {2637--2646},
  publisher = {American Geophysical Union},
  month     = jun,
  year      = {1978},
  doi       = {10.1029/JA083iA06p02637}
}
```

### Mitra2021CPS

```bibtex
@book{Mitra2021CPS,
  author    = {Sayan Mitra},
  title     = {Verifying Cyber-Physical Systems: A Path to Safe Autonomy},
  publisher = {MIT Press},
  address   = {Cambridge, MA, USA},
  year      = {2021},
  isbn      = {9780262044806}
}
```

### dryvr (CAV 2017 version, recommended; same key so \cite sites need no change)

```bibtex
@inproceedings{dryvr,
  author    = {Chuchu Fan and Bolun Qi and Sayan Mitra and Mahesh Viswanathan},
  title     = {{DryVR}: Data-Driven Verification and Compositional Reasoning for Automotive Systems},
  booktitle = {Computer Aided Verification (CAV 2017)},
  editor    = {Rupak Majumdar and Viktor Kun{\v{c}}ak},
  series    = {Lecture Notes in Computer Science},
  volume    = {10426},
  pages     = {441--461},
  publisher = {Springer},
  address   = {Cham},
  year      = {2017},
  doi       = {10.1007/978-3-319-63387-9_22}
}
```

CoRR version, if the preprint is what is meant (use a different key if both are kept):

```bibtex
@article{dryvr-arxiv,
  author        = {Chuchu Fan and Bolun Qi and Sayan Mitra and Mahesh Viswanathan},
  title         = {{DryVR}: Data-Driven Verification and Compositional Reasoning for Automotive Systems},
  journal       = {CoRR},
  volume        = {abs/1702.06902},
  year          = {2017},
  eprint        = {1702.06902},
  archiveprefix = {arXiv},
  url           = {https://arxiv.org/abs/1702.06902}
}
```

### dunlap2023rta

The third author's given name is "Kaiden" in AIAA's deposited record for the journal article and "Kai" in AIAA's record for the SciTech 2022 version; confirm against the journal PDF before choosing.

```bibtex
@article{dunlap2023rta,
  author    = {Kyle Dunlap and Mark Mote and Kaiden Delsing and Kerianne L. Hobbs},
  title     = {Run Time Assured Reinforcement Learning for Safe Satellite Docking},
  journal   = {Journal of Aerospace Information Systems},
  volume    = {20},
  number    = {1},
  pages     = {25--36},
  publisher = {American Institute of Aeronautics and Astronautics},
  month     = jan,
  year      = {2023},
  doi       = {10.2514/1.I011126}
}
```

### erwin-cdc16

```bibtex
@inproceedings{erwin-cdc16,
  author    = {Christopher Jewison and R. Scott Erwin},
  title     = {A Spacecraft Benchmark Problem for Hybrid Control and Estimation},
  booktitle = {2016 IEEE 55th Conference on Decision and Control (CDC)},
  pages     = {3300--3305},
  publisher = {IEEE},
  address   = {Las Vegas, NV, USA},
  month     = dec,
  year      = {2016},
  doi       = {10.1109/CDC.2016.7798765}
}
```

### li2023verse

```bibtex
@inproceedings{li2023verse,
  author    = {Yangge Li and Haoqing Zhu and Katherine Braught and Keyi Shen and Sayan Mitra},
  title     = {Verse: A {Python} Library for Reasoning About Multi-agent Hybrid System Scenarios},
  booktitle = {Computer Aided Verification (CAV 2023)},
  editor    = {Constantin Enea and Akash Lal},
  series    = {Lecture Notes in Computer Science},
  volume    = {13964},
  pages     = {351--364},
  publisher = {Springer},
  address   = {Cham},
  year      = {2023},
  doi       = {10.1007/978-3-031-37706-8_18}
}
```

### miller2024satellite

```bibtex
@inproceedings{miller2024satellite,
  author    = {Kristina Miller and Sean Phillips and Sayan Mitra},
  title     = {Guaranteed Safe Satellite Guidance and Navigation Using Reachability Based Switching Controllers},
  booktitle = {2024 American Control Conference (ACC)},
  pages     = {2298--2303},
  publisher = {IEEE},
  address   = {Toronto, ON, Canada},
  month     = jul,
  year      = {2024},
  doi       = {10.23919/ACC60939.2024.10644961}
}
```

### rdvzvis

```bibtex
@inproceedings{rdvzvis,
  author    = {Jingjin Yu and Steven M. LaValle and Daniel Liberzon},
  title     = {Rendezvous Without Coordinates},
  booktitle = {2008 47th IEEE Conference on Decision and Control (CDC)},
  pages     = {1803--1808},
  publisher = {IEEE},
  address   = {Cancun, Mexico},
  month     = dec,
  year      = {2008},
  doi       = {10.1109/CDC.2008.4739343}
}
```

### scipy_2020

```bibtex
@article{scipy_2020,
  author    = {Pauli Virtanen and Ralf Gommers and Travis E. Oliphant and Matt Haberland and Tyler Reddy and David Cournapeau and Evgeni Burovski and Pearu Peterson and Warren Weckesser and Jonathan Bright and St{\'e}fan J. {van der Walt} and Matthew Brett and Joshua Wilson and K. Jarrod Millman and Nikolay Mayorov and Andrew R. J. Nelson and Eric Jones and Robert Kern and Eric Larson and C J Carey and {\.I}lhan Polat and Yu Feng and Eric W. Moore and Jake VanderPlas and Denis Laxalde and Josef Perktold and Robert Cimrman and Ian Henriksen and E. A. Quintero and Charles R. Harris and Anne M. Archibald and Ant{\^o}nio H. Ribeiro and Fabian Pedregosa and Paul {van Mulbregt} and {SciPy 1.0 Contributors}},
  title     = {{SciPy} 1.0: Fundamental Algorithms for Scientific Computing in {Python}},
  journal   = {Nature Methods},
  volume    = {17},
  number    = {3},
  pages     = {261--272},
  publisher = {Nature Publishing Group},
  month     = mar,
  year      = {2020},
  doi       = {10.1038/s41592-019-0686-2}
}
```

### stanleycar

```bibtex
@inproceedings{stanleycar,
  author    = {Gabriel M. Hoffmann and Claire J. Tomlin and Michael Montemerlo and Sebastian Thrun},
  title     = {Autonomous Automobile Trajectory Tracking for Off-Road Driving: Controller Design, Experimental Validation and Racing},
  booktitle = {2007 American Control Conference (ACC)},
  pages     = {2296--2301},
  publisher = {IEEE},
  address   = {New York, NY, USA},
  month     = jul,
  year      = {2007},
  doi       = {10.1109/ACC.2007.4282788}
}
```

### z3

```bibtex
@inproceedings{z3,
  author    = {Leonardo {de Moura} and Nikolaj Bj{\o}rner},
  title     = {{Z3}: An Efficient {SMT} Solver},
  booktitle = {Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2008)},
  editor    = {C. R. Ramakrishnan and Jakob Rehof},
  series    = {Lecture Notes in Computer Science},
  volume    = {4963},
  pages     = {337--340},
  publisher = {Springer},
  address   = {Berlin, Heidelberg},
  year      = {2008},
  doi       = {10.1007/978-3-540-78800-3_24}
}
```

### zhang2018efficientneuralnetworkrobustness

Page range omitted: NeurIPS's own BibTeX export for this paper has an empty `pages` field, and no other primary source was reachable in this session.

```bibtex
@inproceedings{zhang2018efficientneuralnetworkrobustness,
  author    = {Huan Zhang and Tsui-Wei Weng and Pin-Yu Chen and Cho-Jui Hsieh and Luca Daniel},
  title     = {Efficient Neural Network Robustness Certification with General Activation Functions},
  booktitle = {Advances in Neural Information Processing Systems 31 (NeurIPS 2018)},
  editor    = {S. Bengio and H. Wallach and H. Larochelle and K. Grauman and N. Cesa-Bianchi and R. Garnett},
  volume    = {31},
  publisher = {Curran Associates, Inc.},
  year      = {2018},
  url       = {https://proceedings.neurips.cc/paper/2018/hash/d04863f100d59b3eb688a11f95b0ae60-Abstract.html}
}
```

### nasa2020ae

```bibtex
@misc{nasa2020ae,
  author       = {{NASA}},
  title        = {Crew {D}ragon Exits Station's Approach Ellipsoid},
  howpublished = {NASA Commercial Crew Program blog, August 1, 2020. Original URL \url{https://blogs.nasa.gov/commercialcrew/2020/08/01/crew-dragon-exits-stations-approach-ellipsoid-2/} (no longer served); archived at \url{https://web.archive.org/web/20200807001726/https://blogs.nasa.gov/commercialcrew/2020/08/01/crew-dragon-exits-stations-approach-ellipsoid-2/}},
  year         = {2020},
  month        = aug,
  note         = {Archived copy accessed October 2026}
}
```

## Notes on method and limits

- DOIs were checked by fetching the Crossref registry record for the exact DOI string; each record's title and authors were compared with the entry. One DOI (Hobbs2020) resolves to an unrelated paper.
- EPiC volume, pages, and author lists were read from the EasyChair volume pages reached by resolving the EPiC DOIs; the Crossref `page` field for EPiC records is garbled (it stores first page and page count) and was not used.
- LNCS volume numbers and editors were read from the Springer chapter pages.
- DBLP (all mirrors), the ACM DL, arc.aiaa.org and mitpress.mit.edu returned bot-protection or 403 responses to every fetch attempted here. The two fields left unverified because of this are the NeurIPS 2018 page range and the printed spelling of the Dunlap third author.
- The CORA replacement follows the instruction to cite the ARCH 2015 paper. If the experiments used a specific CORA release, the authors may also want to name that release in the text; the manual itself is not a citable publication.
