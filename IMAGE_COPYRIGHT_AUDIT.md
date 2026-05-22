# Image Copyright Audit — Legacy & Medium Blog Posts

**Date:** 2026-05-22
**Scope:** ~454 images across `next-site/public/blog/legacy-posts-and-images/` (2008–2016) and `next-site/public/blog/aws-medium-posts-and-images/` (2016–2021). Every image was inspected visually.
**Result:** **127 images flagged** for copyright review (≈51 High, ≈58 Medium, ≈18 Low).

> **Method note:** "Could be copyrighted" is a heuristic flag, not a legal determination. Flagged = the image is likely third-party intellectual property (logos, product/website screenshots, stock photos, movie/TV stills, cartoons, book/album covers, paper figures, photos of public figures). The author's own diagrams, code/terminal screenshots, AWS-console captures, his own photos, his own book covers, and public-domain artwork were **not** flagged.
>
> **Overlap caveat:** the `2017-09-*` posts were covered by two auditors; duplicates are removed below. `2017-09-10_Keras-shoot-out--part-3/image01.webp` got conflicting descriptions ("Fast & Furious car chase" vs. "western, cowboy with rifle") — confirm the exact film on review; it is a movie still either way.

---

## Recommended priority

1. **Fix the "hook image" habit first.** ~45 of the 51 High-risk items are decorative opening images that are movie/TV stills or celebrity photos. They are not load-bearing — replace each with an original or properly-licensed image (or remove). This single batch clears most of the exposure.
2. **Third-party website screenshots (2010 Currys/Dixons/PC World/Pixmania)** — High risk; these display brand logos and product photography. Consider removing or cropping to the author's own work only.
3. **Paper figures / vendor diagrams (Medium risk)** — add explicit source attribution where missing, or redraw.
4. **Low-risk items** — review only if you want to be strict.

---

## HIGH risk (≈51) — act on these

### Legacy posts
| Path (from repo root) | Shows | Category |
|---|---|---|
| next-site/public/blog/legacy-posts-and-images/2010/2010-02-15-new-currys-website-live-image-01.webp | Currys retail website (Norton, LG product imagery) | 3rd-party website + logos |
| next-site/public/blog/legacy-posts-and-images/2010/2010-03-01-new-dixons-website-live-image-02.webp | Dixons retail website (Samsung, LG) | 3rd-party website + logos |
| next-site/public/blog/legacy-posts-and-images/2010/2010-03-01-new-pc-world-website-live-image-02.webp | PC World website (Logitech, Apple, Microsoft) | 3rd-party website + logos |
| next-site/public/blog/legacy-posts-and-images/2010/2010-05-19-new-pixmania-pixmania-pro-websites-image-01.webp | Pixmania-Pro website (camera brand imagery) | 3rd-party website + logos |
| next-site/public/blog/legacy-posts-and-images/2010/2010-05-19-new-pixmania-pixmania-pro-websites-image-04.webp | Pixmania.com website (Samsung, Panasonic, Apple) | 3rd-party website + logos |
| next-site/public/blog/legacy-posts-and-images/2011/2011-07-04-code-review-criteo-image-03.webp | "WTFs/minute" code-quality cartoon — visible "(c) 2008 Focus Shift/OSNews/Thom Holwerda" | Cartoon (explicit © notice) |
| next-site/public/blog/legacy-posts-and-images/2013/2013-08-05-nodejs-part-4-the-big-kahuna-syslog-image-02.webp | Samuel L. Jackson — still from "Pulp Fiction" | Movie still + celebrity |

### Medium posts — movie/TV stills & memes (the "hook image" cluster)
| Path (from repo root) | Shows |
|---|---|
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-05_Fascinating-Tales-of-a-Strange-Tomorrow/image01.webp | Robby the Robot — "Forbidden Planet" (1956) |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-05_Fascinating-Tales-of-a-Strange-Tomorrow/image09.webp | HAL 9000 eye — "2001: A Space Odyssey" |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-10_An-introduction-to-the-MXNet-API---part-2/image01.webp | Yoda "There Is Another" meme (Star Wars; quickmeme watermark) |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-09-03_Keras-shoot-out--TensorFlow-vs-MXNet/image01.webp | Clint Eastwood — "The Good, the Bad and the Ugly" |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-09-08_Keras-shoot-out--part-2--a-deeper-look-at-memory-usage/image01.webp | Eli Wallach — "The Good, the Bad and the Ugly" |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-09-09_Speeding-up-Apache-MXNet-with-the-NNPACK-library/image01.webp | Movie still — man driving at night (action film) |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-09-10_Keras-shoot-out--part-3--fine-tuning/image01.webp | Movie still — conflicting IDs ("Fast & Furious" / western); confirm |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-09-15_Speeding-up-Apache-MXNet-with-the-NNPACK-library--Raspberry-Pi-edition-/image01.webp | Movie still — car on fire mid-chase ("Fast & Furious") |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-09-19_ImageNet---part-1--going-on-an-adventure/image01.webp | "The Hobbit" — Bilbo in the Shire |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-09-24_ImageNet---part-2--the-road-goes-ever-on-and-on/image04.webp | "The Lord of the Rings" — Frodo & Sam |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-10-09_Building-FPGA-applications-on-AWS---and-yes--for-Deep-Learning-too/image06.webp | "Game of Thrones" — The Mountain |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-11-17_Speeding-up-Apache-MXNet--part-3--let-s-smash-it-with-C5-and-Intel-MKL/image01.webp | "The Avengers" — the Hulk |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-12-18_Building-a-spam-classifier--PySpark-MLLib-vs-SageMaker-XGBoost/image01.webp | "Rocky IV" — Rocky vs. Drago |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-12-19_Exploring--ahem--AWS-DeepLens/image02.webp | "What is this new devilry" LOTR meme (quickmeme watermark) |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-01-12_10-steps-on-the-road-to-Deep-Learning--part-1-/image01.webp | "The Lord of the Rings" still |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-01-15_10-steps-on-the-road-to-Deep-Learning--part-2-/image01.webp | "The Lord of the Rings" — Army of the Dead |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-01-19_Options-for-Machine-Translation-on-AWS--/image01.webp | "Lost in Translation" — Bill Murray |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-01-26_Resurrecting-a-BrickLens/image01.webp | "Young Frankenstein" — "It's Alive!" |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-01-29_Building-a-movie-recommender-with-Factorization-Machines-on-Amazon-SageMaker/image02.webp | "What We Do in the Shadows" promotional still |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-03-14_Tumbling-down-the-SGD-rabbit-hole---part-1/image02.webp | Disney "Alice in Wonderland" animation still |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-03-17_Tumbling-down-the-SGD-rabbit-hole---part-2/image03.webp | "Dr. Strangelove" — Peter Sellers |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-03-17_Tumbling-down-the-SGD-rabbit-hole---part-2/image04.webp | The Ramones — live concert photo |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-03-17_Tumbling-down-the-SGD-rabbit-hole---part-2/image07.webp | Monty Python sketch still |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-04-26_Using-Chalice-to-serve-SageMaker-predictions/image01.webp | "Monty Python and the Holy Grail" still |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-05-08_Apache-Spark-and-Amazon-SageMaker-the-best-of-both-worlds---part-1/image02.webp | "Avengers: Infinity War" — Thanos / Infinity Gauntlet |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-05-14_Retraining-SageMaker-models-with-Chalice-and-Serverless/image01.webp | Dwayne "The Rock" Johnson (captioned "Sorry, Rock") |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-06-01_Apache-MXNet-as-a-backend-for-Keras-2/image01.webp | "Ghost Rider" film still |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-06-01_Gluon-CV--add-image-classification-and-object-detection-to-your-applications/image02.webp | "The Terminator" — vision overlay |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-06-04_Training-with-PyTorch-on-Amazon-SageMaker/image02.webp | "The Lord of the Rings" — orc with torch |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-07-28_Mastering-the-mystical-art-of-model-deployment/image03.webp | "Doctor Strange" animated GIF (Marvel) |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-07-28_Mastering-the-mystical-art-of-model-deployment/image07.webp | "The Lord of the Rings" — Gandalf reading |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-11-29_Thoughts-on-the-beta-Machine-Learning-certification/image01.webp | "Game of Thrones" — Samwell Tarly in the library |
| next-site/public/blog/aws-medium-posts-and-images/2019/2019-01-10_Applying-Machine-Learning-to-AWS-services/image01.webp | "WarGames" — WOPR terminal (moviepilot watermark) |
| next-site/public/blog/aws-medium-posts-and-images/2019/2019-01-29_Scaling-Machine-Learning-from-0-to-millions-of-users--part-1/image01.webp | Movie still — close-up of a young girl |
| next-site/public/blog/aws-medium-posts-and-images/2019/2019-01-29_Scaling-Machine-Learning-from-0-to-millions-of-users--part-1/image02.webp | Arnold Schwarzenegger — "Conan the Barbarian" (yourprops watermark) |
| next-site/public/blog/aws-medium-posts-and-images/2019/2019-01-29_Scaling-Machine-Learning-from-0-to-millions-of-users--part-1/image03.webp | "Conan the Barbarian" — wheel-of-pain scene |
| next-site/public/blog/aws-medium-posts-and-images/2019/2019-05-20_Mastering-the-mystical-art-of-model-deployment-with-Amazon-SageMaker/image02.webp | "Doctor Strange" animated GIF (shrlockspeare tumblr watermark) |
| next-site/public/blog/aws-medium-posts-and-images/2019/2019-07-20_Doctor-Alice-and-Cloud-Native-Bob--my-favorite-Machine-Learning-users/image01.webp | Movie/TV still — actor in a study |
| next-site/public/blog/aws-medium-posts-and-images/2019/2019-11-26_Pre-Invent-2019---Time-to-catch-up-/image01.webp | "Game of Thrones" — Samwell Tarly carrying books |

### Medium posts — celebrities, book covers, fine art
| Path (from repo root) | Shows |
|---|---|
| next-site/public/blog/aws-medium-posts-and-images/2016/2016-11-30_A-hands-on-look-at-the-Amazon-Rekognition-API/image01.webp | 1986 World Cup match (Maradona) — famous press photo |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-05_Fascinating-Tales-of-a-Strange-Tomorrow/image04.webp | Photo of Marvin Minsky (public figure) |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-05_Fascinating-Tales-of-a-Strange-Tomorrow/image06.webp | "I, Robot" (Asimov) — Signet paperback cover |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-05_Fascinating-Tales-of-a-Strange-Tomorrow/image07.webp | Photo of Arthur C. Clarke (public figure) |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-05-19_Create-your-own-Basquiat-with-Apache-MXNet-and-Generative-Adversarial-Networks/image07.webp | An actual Jean-Michel Basquiat painting |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-07-02_10-Deep-Learning-projects-based-on-Apache-MXNet/image02.webp | Djokovic, Federer, Nadal, Murray — press photos |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-07-02_10-Deep-Learning-projects-based-on-Apache-MXNet/image04.webp | Group of Chinese celebrities at an event — press photo |

---

## MEDIUM risk (≈58) — review / attribute / redraw

### Legacy posts
| Path (from repo root) | Shows |
|---|---|
| next-site/public/blog/legacy-posts-and-images/2008/2008-12-22-howto-compiling-mediatomb-ffmpegthumbnailer-all-li-image-02.webp | PS3 XMB UI + album track metadata |
| next-site/public/blog/legacy-posts-and-images/2008/2008-12-22-howto-compiling-mediatomb-ffmpegthumbnailer-all-li-image-03.webp | PS3 UI + album cover art thumbnails |
| next-site/public/blog/legacy-posts-and-images/2008/2008-12-24-mediatomb-012-on-ps3-video-thumbnails-youtube-and--image-02.webp | PS3 UI + album metadata |
| next-site/public/blog/legacy-posts-and-images/2008/2008-12-24-mediatomb-012-on-ps3-video-thumbnails-youtube-and--image-05.webp | PS3 UI + album art thumbnails |
| next-site/public/blog/legacy-posts-and-images/2008/2008-12-24-mediatomb-012-on-ps3-video-thumbnails-youtube-and--image-06.webp | PS3 UI listing 3rd-party car videos |
| next-site/public/blog/legacy-posts-and-images/2008/2008-12-24-mediatomb-012-on-ps3-video-thumbnails-youtube-and--image-11.webp | PS3 UI + 3rd-party YouTube video listing |
| next-site/public/blog/legacy-posts-and-images/2008/2008-12-24-mediatomb-012-on-ps3-video-thumbnails-youtube-and--image-14.webp | PS3 UI listing Apple movie trailers |
| next-site/public/blog/legacy-posts-and-images/2008/2008-12-24-mediatomb-012-on-ps3-video-thumbnails-youtube-and--image-19.webp | Movie/TV still (castle + wave) |
| next-site/public/blog/legacy-posts-and-images/2008/2008-12-24-mediatomb-012-on-ps3-video-thumbnails-youtube-and--image-25.webp | PS3 UI + Megadeth album-art filmstrip |
| next-site/public/blog/legacy-posts-and-images/2009/2009-01-23-howto-h264-youtube-videos-in-mediatomb-...-image-03.webp | PS3 UI + album metadata (verify exact filename) |
| next-site/public/blog/legacy-posts-and-images/2009/2009-01-23-howto-h264-youtube-videos-in-mediatomb-...-image-04.webp | Concert footage still — bass guitarist |
| next-site/public/blog/legacy-posts-and-images/2010/2010-09-08-new-pixmania-pro-websites-image-01.webp | Pixmania-Pro logo over a Europe map |
| next-site/public/blog/legacy-posts-and-images/2012/2012-08-30-viking-laws-...-part-2-image-01.webp | Costumed Viking warrior (film still / stock) |
| next-site/public/blog/legacy-posts-and-images/2012/2012-08-31-viking-laws-...-part-3-image-02.webp | Painting of a Viking longship |
| next-site/public/blog/legacy-posts-and-images/2013/2013-09-25-viking-laws-...-part-7-image-01.webp | Illustration of a Viking village raid |
| next-site/public/blog/legacy-posts-and-images/2013/2013-08-17-nodejs-part-51-dont-you-c-image-01.webp | Disco-dancers clip-art |
| next-site/public/blog/legacy-posts-and-images/2013/2013-08-21-arduino-lcd-thermometer-image-01.webp | Fritzing breadboard diagram + Arduino trademark |
| next-site/public/blog/legacy-posts-and-images/2014/2014-05-13-aldebaran-aws-summit-paris-2014-image-01.webp | Aldebaran NAO robot — product/press photo |
| next-site/public/blog/legacy-posts-and-images/2015/2015-03-19-java-8-and-lambdas-...-image-01.webp | "Lambda Lambda Lambda" logo (from "Revenge of the Nerds") |

> Some legacy 2009 filenames are abbreviated above (`...`); confirm exact names in `legacy-posts-and-images/2009/` before editing.

### Medium posts — paper figures, vendor diagrams, 3rd-party screenshots, stock/concert photos
| Path (from repo root) | Shows |
|---|---|
| next-site/public/blog/aws-medium-posts-and-images/2016/2016-11-30_A-hands-on-look-at-the-Amazon-Rekognition-API/image05.webp | Tokyo Shinjuku neon street — stock + 3rd-party billboards |
| next-site/public/blog/aws-medium-posts-and-images/2016/2016-11-30_A-hands-on-look-at-the-Amazon-Rekognition-API/image07.webp | Oktoberfest beer-hall crowd — stock photo |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-05_Fascinating-Tales-of-a-Strange-Tomorrow/image02.webp | Richard Greenblatt at an IBM 7094 — archival press photo |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-05_Fascinating-Tales-of-a-Strange-Tomorrow/image03.webp | Multilayer NN diagram — reproduced from a textbook/paper |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-05_Fascinating-Tales-of-a-Strange-Tomorrow/image05.webp | Archival photo — researcher at a computer |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-05_Fascinating-Tales-of-a-Strange-Tomorrow/image08.webp | LeNet-style CNN diagram — reproduced from a paper |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-05_Fascinating-Tales-of-a-Strange-Tomorrow/image11.webp | Single-neuron diagram — reproduced from a textbook |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-06_FreeBSD--from-CD-ROM-to-Cloud/image09.webp | Photo of 3rd-party software CD-ROM jewel cases (cover art) |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-14_An-introduction-to-the-MXNet-API---part-4/image01.webp | Concert photo of a metal guitarist ("Source: metaltraveller.com") |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-14_An-introduction-to-the-MXNet-API---part-4/image02.webp | Same concert photo — green-channel crop |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-14_An-introduction-to-the-MXNet-API---part-4/image03.webp | Same concert photo — red-channel crop |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-14_An-introduction-to-the-MXNet-API---part-4/image04.webp | Same concert photo — blue-channel crop |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-15_An-introduction-to-the-MXNet-API---part-5/image01.webp | Child playing violin — stock-style photo |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-15_An-introduction-to-the-MXNet-API---part-5/image03.webp | LeNet CNN diagram — paper figure |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-06-08_Apache-MXNet-support-in-Keras/image01.webp | Screenshot of a François Chollet tweet (Twitter UI + person) |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-07-02_10-Deep-Learning-projects-based-on-Apache-MXNet/image05.webp | COCO/VOC sample images — 3rd-party benchmark dataset |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-10-09_Building-FPGA-applications-on-AWS---and-yes--for-Deep-Learning-too/image04.webp | Diagram embedding a Xilinx UltraScale FPGA product photo |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-10-09_Building-FPGA-applications-on-AWS---and-yes--for-Deep-Learning-too/image07.webp | NN-to-FPGA-slices figure — reproduced from a paper/source |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-10-09_Building-FPGA-applications-on-AWS---and-yes--for-Deep-Learning-too/image08.webp | "Moore's Law" transistor/clock-speed chart — 3rd-party graphic |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-10-09_Building-FPGA-applications-on-AWS---and-yes--for-Deep-Learning-too/image11.webp | Xilinx SDAccel marketing/architecture diagram |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-11-07_10--more--Deep-Learning-projects-based-on-Apache-MXNet/image01.webp | DenseNet "Figure 1" — reproduced from an academic paper |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-11-07_10--more--Deep-Learning-projects-based-on-Apache-MXNet/image05.webp | iOS app demo screenshot — 3rd-party GitHub project |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-11-07_10--more--Deep-Learning-projects-based-on-Apache-MXNet/image07.webp | STN-OCR demo output — 3rd-party academic project (Bartz et al.) |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-11-07_10--more--Deep-Learning-projects-based-on-Apache-MXNet/image08.webp | OpenPose pose-estimation demo — 3rd-party project (Cao et al.) |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-11-13_Generative-Adversarial-Networks-on-Apache-MXNet--part-1/image02.webp | DCGAN generator diagram — "Adapted from arxiv.org/pdf/1511.06434.pdf" |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-11-13_Generative-Adversarial-Networks-on-Apache-MXNet--part-1/image07.webp | DCGAN discriminator diagram — adapted from same arXiv paper |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-12-19_Exploring--ahem--AWS-DeepLens/image03.webp | Stock photo of a tiger (ImageNet-style demo input) |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-12-19_Exploring--ahem--AWS-DeepLens/image05.webp | Intel OpenVINO Model Optimizer workflow diagram (Intel-branded) |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-01-16_Image-classification-on-Amazon-SageMaker/image01.webp | Browser screenshot embedding a Pixabay stock dog photo |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-02-25_Yet-another-10-Deep-Learning-projects-based-on-Apache-MXNet/image02.webp | Faces dataset / 3D face reconstruction figure (likely a paper) |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-03-17_Tumbling-down-the-SGD-rabbit-hole---part-2/image02.webp | Optimizer training-loss plot — FTML academic paper figure |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-03-17_Tumbling-down-the-SGD-rabbit-hole---part-2/image06.webp | Optimizer accuracy plot — academic paper figure |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-03-17_Tumbling-down-the-SGD-rabbit-hole---part-2/image08.webp | Optimizer training-loss plot — FTML paper figure |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-04-06_AWS-Summit-San-Francisco--AI-ML-recap/image01.webp | San Francisco fireworks — stock-style photography |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-06-01_Gluon-CV--add-image-classification-and-object-detection-to-your-applications/image03.webp | Live concert photo of a metal guitarist (identifiable person) |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-06-01_Gluon-CV--add-image-classification-and-object-detection-to-your-applications/image04.webp | Lamborghini Huracán at an auto show (prominent logos) |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-06-01_Gluon-CV--add-image-classification-and-object-detection-to-your-applications/image05.webp | Object detection on a White House interior — 3rd-party press/stock photo |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-06-07_Johnny-Pi--I-am-your-father---part-7/image05.webp | Carrie Fisher (celebrity) on a printed book page — verify exact folder/file |
| next-site/public/blog/aws-medium-posts-and-images/2019/2019-12-19_Annotating-Image-Datasets-with-Amazon-SageMaker-Ground-Truth/image01.webp | Concert photo of a band (looks like Slayer) — identifiable musicians |

> Several Medium-risk filenames (the 2009 PS3 posts, the Johnny-Pi part-7 image) are reconstructed from auditor reports — confirm exact paths before editing.

---

## LOW risk (≈18) — review only if being strict

| Path (from repo root) | Shows | Note |
|---|---|---|
| next-site/public/blog/legacy-posts-and-images/2008/2008-12-22-howto-compiling-mediatomb-ffmpegthumbnailer-all-li-image-06.webp | PS3 "MediaTomb" XMB menu | 3rd-party UI chrome only |
| next-site/public/blog/legacy-posts-and-images/2008/2008-12-24-mediatomb-012-on-ps3-video-thumbnails-youtube-and--image-12.webp | PS3 XMB Favorites menu | UI chrome only |
| next-site/public/blog/legacy-posts-and-images/2008/2008-12-24-mediatomb-012-on-ps3-video-thumbnails-youtube-and--image-13.webp | PS3 XMB menu | UI chrome only |
| next-site/public/blog/legacy-posts-and-images/2008/2008-12-24-mediatomb-012-on-ps3-video-thumbnails-youtube-and--image-17.webp | PS3 UI + video thumbnails | minor |
| next-site/public/blog/legacy-posts-and-images/2008/2008-12-24-mediatomb-012-on-ps3-video-thumbnails-youtube-and--image-21.webp | PS3 "All Trailers" menu | UI chrome only |
| next-site/public/blog/legacy-posts-and-images/2008/2008-12-24-mediatomb-012-on-ps3-video-thumbnails-youtube-and--image-22.webp | PS3 UI + video thumbnails | minor |
| next-site/public/blog/legacy-posts-and-images/2008/2008-12-24-mediatomb-012-on-ps3-video-thumbnails-youtube-and--image-24.webp | PS3 "Most Viewed / Top Rated" menu | UI chrome only |
| next-site/public/blog/legacy-posts-and-images/2012/2012-09-05-viking-laws-...-part-5-image-02.webp | Viking longship dragon-head prow | stock photo |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-09_An-introduction-to-the-MXNet-API---part-1/image05.webp | "Subscribe" robot graphic — Medium publication footer | publisher boilerplate |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-09_An-introduction-to-the-MXNet-API---part-1/image06.webp | "Apply To Be A Writer" graphic — publication footer | publisher boilerplate |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-09_An-introduction-to-the-MXNet-API---part-1/image07.webp | "Join the Community" graphic — publication footer | publisher boilerplate |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-16_An-introduction-to-the-MXNet-API---part-6/image01.webp | Photo of a Samsung TV remote control | branded product, minor |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-08-28_Johnny-Pi--I-am-your-father---part-2--the-joystick/image01.webp | SparkFun joystick breakout — vendor product photo | minor |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-09-17_Johnny-Pi--I-am-your-father---part-5--adding-MXNet-for-local-image-classification/image03.webp | Sony PS3 DualShock controller photo | branded product, minor |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-11-06_Enabling-Deep-Learning-in-IoT-applications-with-Apache-MXNet/image01.webp | Michelangelo "Creation of Adam" | public-domain artwork (reproduction rights only) |
| next-site/public/blog/aws-medium-posts-and-images/2017/2017-12-23_Amazon-AI--the-Christmas-post/image01.webp | Bruegel "The Tower of Babel" | public-domain artwork (reproduction rights only) |
| next-site/public/blog/aws-medium-posts-and-images/2018/2018-03-17_Tumbling-down-the-SGD-rabbit-hole---part-2/image01.webp | Optimizer trajectory animation plot | commonly reproduced from a blog |

The "Subscribe / Apply To Be A Writer / Join the Community" robot graphics recur across many 2017 Medium posts — they are Medium-publication template assets (low commercial risk; likely licensed by the publisher, not the author).

---

## Not flagged (low risk — confirmed safe)

- Author's own architecture / process diagrams and hand-drawn diagrams
- Author's own code, terminal, `nvidia-smi`, `htop`, `docker` screenshots
- AWS console screenshots, AWS Marketplace UI, AWS service icons, AWS slide-deck graphics
- Author's own photos (himself speaking, his hardware, colleagues, office)
- His own published book covers — *Learn Amazon SageMaker* 1st & 2nd ed. (Packt)
- Standard public ML datasets shown as-is: MNIST, Fashion-MNIST, CIFAR-10
- Amazon's own product photos (Echo Dot, etc.)

## Borderline items deliberately NOT flagged (noted for completeness)

- `legacy/2012/2012-04-27-...-image-01.webp` — Criteo "Code of Duty 2" recruiting poster: the author's *employer's* own marketing material, but it visually parodies the Call of Duty game brand. Employer asset → not flagged; revisit if strict.
- `2017-12-19_Exploring--ahem--AWS-DeepLens/image06.webp` — author's own object-detection demo photo of a real-world billboard; minor incidental third-party branding (Bombay Sapphire). Not flagged.
- Johnny-Pi architecture diagrams across multiple posts embed a small Twitter bird logo and an Arduino board icon — de minimis third-party logos inside the author's own diagrams. Not flagged.
