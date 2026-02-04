export interface Computer {
  name: string;
  year: string;
  cpu: string;
  ram: string;
  description?: string;
  image?: string;
  wikiUrl?: string;
  software?: string;
}

export interface UnixBook {
  title: string;
  author: string;
  year: string;
  image?: string;
  description: string;
}

export interface VintageCD {
  title: string;
  year: string;
  description: string;
}

export const COMPUTERS: Computer[] = [
  {
    name: 'Commodore PET CBM 2001',
    year: '1977',
    cpu: 'MOS 6502 @ 1 MHz',
    ram: '4 KB',
    image: '/assets/computers/commodore-pet-2001.webp',
    wikiUrl: 'https://en.wikipedia.org/wiki/Commodore_PET',
    software: 'Commodore BASIC 1.0',
  },
  {
    name: 'Commodore VIC-20',
    year: '1980',
    cpu: 'MOS 6502 @ 1 MHz',
    ram: '5 KB',
    image: '/assets/computers/commodore-vic20.webp',
    wikiUrl: 'https://en.wikipedia.org/wiki/Commodore_VIC-20',
    software: 'Commodore BASIC 2.0',
  },
  {
    name: 'Apple IIe',
    year: '1983',
    cpu: '65C02 @ 1.023 MHz',
    ram: '64 KB',
    image: '/assets/computers/apple-iie.webp',
    wikiUrl: 'https://en.wikipedia.org/wiki/Apple_IIe',
    software: 'AppleSoft BASIC, ProDOS',
  },
  {
    name: 'Apple IIc',
    year: '1984',
    cpu: '65C02 @ 1.4 MHz',
    ram: '128 KB',
    image: '/assets/computers/apple-iic.webp',
    wikiUrl: 'https://en.wikipedia.org/wiki/Apple_IIc',
    software: 'AppleSoft BASIC, ProDOS',
  },
  {
    name: 'Amstrad CPC464',
    year: '1984',
    cpu: 'Zilog Z80 @ 4 MHz',
    ram: '64 KB',
    image: '/assets/computers/amstrad-cpc464.webp',
    wikiUrl: 'https://en.wikipedia.org/wiki/Amstrad_CPC',
    software: 'Locomotive BASIC, AMSDOS',
  },
  {
    name: 'IBM PC XT (Transportable)',
    year: '1983',
    cpu: 'Intel 8088 @ 4.77 MHz',
    ram: '128-640 KB',
    image: '/assets/computers/ibm-pc-xt.webp',
    wikiUrl: 'https://en.wikipedia.org/wiki/IBM_Personal_Computer_XT',
    software: 'PC-DOS 2.0',
  },
  {
    name: 'IBM PC Convertible (5140)',
    year: '1986',
    cpu: 'Intel 80C88 @ 4.77 MHz',
    ram: '256 KB',
    image: '/assets/computers/ibm-pc-convertible.webp',
    wikiUrl: 'https://en.wikipedia.org/wiki/IBM_PC_Convertible',
    software: 'PC-DOS 3.2',
  },
  {
    name: 'Macintosh SE/30',
    year: '1989',
    cpu: 'Motorola 68030 @ 16 MHz',
    ram: '1-128 MB',
    image: '/assets/computers/macintosh-se30.webp',
    wikiUrl: 'https://en.wikipedia.org/wiki/Macintosh_SE/30',
    software: 'System 6.0.3 - System 7.5.5',
  },
  {
    name: 'Macintosh IIfx',
    year: '1990',
    cpu: 'Motorola 68030 @ 40 MHz',
    ram: 'Up to 128 MB',
    image: '/assets/computers/macintosh-iifx.webp',
    wikiUrl: 'https://en.wikipedia.org/wiki/Macintosh_IIfx',
    software: 'System 6.0.5 - Mac OS 7.6.1',
  },
  {
    name: 'Macintosh PowerBook 180',
    year: '1992',
    cpu: 'Motorola 68030 @ 33 MHz',
    ram: '4-14 MB',
    image: '/assets/computers/powerbook-180.webp',
    wikiUrl: 'https://en.wikipedia.org/wiki/PowerBook_100_series#PowerBook_180',
    software: 'System 7.1 - Mac OS 7.6.1',
  },
];

export const UNIX_JOURNEY = [
  'My UNIX journey began in early 1992 while studying for my Computer Science engineering degree. Rémy Card was teaching the UNIX class, so I got a Linux system running from day 1. The first release I installed was 0.13, which then became 0.95 in March \'92 (the first release with X Window support). I still remember downloading the floppy images from René Cougnenc\'s BBS.',
  'There wasn\'t a lot of Linux documentation at that time... and none in French. So I started writing my own guide, called "Le Guide du Rootard pour Linux (GRL)". I also translated Matt Welsh\'s Linux info sheet with some help from René. For a while, these two documents were the only Linux documentation in French. Shortly after, Rémy, René, and myself co-wrote in Tribunix what is possibly the first magazine article ever published in France on Linux.',
  'During that time, I got to meet Linus Torvalds a few times. I also attended the 1st Linux Conference in Heidelberg in \'94 and met Richard Stallman there. By then, I had started to work — which meant that I had less time — and I was also growing increasingly annoyed by the business circus surrounding Linux. In May \'95, I decided to stop maintaining the GRL, with Rémy saying that I "massively contributed to Linux usage in France".',
  'In late \'96, I somehow found the time to work on a French translation of Kirk McKusick\'s 4.4BSD book. This book consumed all my evenings (and many nights) for months. I guess having the privilege to exchange some e-mails with Kirk was worth it all!',
];

export const UNIX_BOOKS: UnixBook[] = [
  {
    title: "Lions' Commentary on UNIX 6th Edition",
    author: 'John Lions',
    year: '1977/1996',
    image: '/assets/computers/lions-commentary.webp',
    description: 'The "Ancient Testament" — commented UNIX V6 kernel code. This book was legendary in the UNIX community, containing the complete source code of UNIX V6 with detailed commentary. It was originally distributed as photocopies until it was finally published in 1996.',
  },
  {
    title: 'The Design of the UNIX Operating System',
    author: 'M.J. Bach',
    year: '1986',
    image: '/assets/computers/design-unix-os.webp',
    description: 'The first proper book on the UNIX kernel (mostly System V Release 2), covering all major topics: process management, file system, I/O, etc. Hardly any code, but lots of detailed explanations, figures and algorithms.',
  },
  {
    title: 'The Design and Implementation of the 4.3BSD UNIX Operating System',
    author: 'Leffler, McKusick, Karels & Quaterman',
    year: '1989',
    image: '/assets/computers/4.3bsd-book.webp',
    description: 'The "Ancient Testament" of BSD — Berkeley UNIX implementation. This book documents the 4.3BSD system and was essential for understanding the Berkeley UNIX variant.',
  },
  {
    title: 'The Design and Implementation of the 4.4BSD Operating System',
    author: 'McKusick, Bostic, Karels, Quarterman',
    year: '1996',
    image: '/assets/computers/4.4bsd-design-implementation.webp',
    description: 'The "New Testament", revised and updated for what is the last UNIX version released by the University of Berkeley. A lot of 4.4BSD code ended up in many UNIces, especially in Open Source versions like NetBSD, FreeBSD, OpenBSD and Linux.',
  },
  {
    title: 'Conception et Implémentation du Système 4.4BSD',
    author: 'French translation by Julien Simon',
    year: '1996',
    image: '/assets/computers/4.4bsd-french.webp',
    description: 'I loved that 4.4BSD book so much that I worked on the French translation... and I lived to regret it :) Try the section "explaining" virtual memory management on the VAX: this one alone almost made me quit!',
  },
  {
    title: 'Advanced Programming in the UNIX Environment',
    author: 'W. Richard Stevens',
    year: '1992',
    image: '/assets/computers/advanced-programming-stevens.webp',
    description: 'The "bible" of UNIX programming — system calls and C library. This book taught me how to write proper UNIX programs, covering everything from basic system calls to advanced topics like signals, IPC, and networking.',
  },
  {
    title: 'UNIX Power Tools',
    author: 'Peek, O\'Reilly & Loukides',
    year: '1993',
    image: '/assets/computers/unix-power-tools-book.webp',
    description: 'Over 1000 pages of UNIX tips, tricks and wizardry. Command line tools, scripting, etc: this book has it all. Ubuntu forums and Google didn\'t exist, remember?',
  },
  {
    title: 'The Magic Garden Explained — UNIX System V Release 4',
    author: 'Goodheart & Cox',
    year: '1994',
    image: '/assets/computers/magic-garden-unix.webp',
    description: 'My favorite kernel book. It\'s about SVR4, the convergence of System V and BSD. What makes it special is that it explains not just what the code does, but why it was designed that way.',
  },
  {
    title: 'UNIX Internals — The New Frontiers',
    author: 'Uresh Vahalia',
    year: '1996',
    image: '/assets/computers/unix-internals-frontiers.webp',
    description: 'All concepts are illustrated with real-life examples taken from all major UNIces: 4.4BSD, SVR4, Solaris, etc. As far as I know, this was the first book to compare different UNIX versions in such detail.',
  },
  {
    title: 'UNIX Internals — A Practical Approach',
    author: 'Steve D. Pate',
    year: '1997',
    image: '/assets/computers/unix-internals-practical.webp',
    description: 'Solely talks about SCO UNIX System 5 Release 3.2 for i386 architectures. A good kernel book if you work(ed) on SCO UNIX.',
  },
  {
    title: 'Solaris Internals — Core Kernel Architecture',
    author: 'Mauro & McDougall',
    year: '2000',
    image: '/assets/computers/solaris-internals.webp',
    description: 'The first book on the Solaris kernel (2.5 to 2.7). I was working for Sun Microsystems at the time, so I particularly enjoyed it.',
  },
  {
    title: 'The Basic Kernel — Source Code Secrets',
    author: 'W. Jolitz and L. Jolitz',
    year: '1991/1996',
    image: '/assets/computers/basic-kernel-jolitz.webp',
    description: 'Documents the port of BSD to the x86 architecture, which became 386BSD. This was the foundation for what later became FreeBSD and NetBSD.',
  },
  {
    title: 'The Design of OS/2',
    author: 'H. Deitel and M. Kogan',
    year: '1992',
    image: '/assets/computers/os2-design-book.webp',
    description: 'Not UNIX but still a very good OS, so superior to Windows at the time. A dry but very serious book on designing a true multitasking OS for the i386. DOS, OS/2, Linux: yeah baby, those were the days :)',
  },
  {
    title: 'Programming under Mach',
    author: 'Boykin, Kirschen, Langerman & LoVerso',
    year: '1993',
    image: '/assets/computers/programming-mach-book.webp',
    description: 'Still not UNIX, but getting closer. A number of proper UNIces have been built over the Mach microkernel, from OSF/1 to MacOS X! I used it in \'94-\'96 when I was working on the MASIX project.',
  },
  {
    title: 'Distributed Systems — Concepts and Design',
    author: 'Coulouris, Dollimore & Kindberg',
    year: '1994',
    image: '/assets/computers/distributed-systems-book.webp',
    description: 'Simply the BEST book on distributed systems. It has the most complete and clearest descriptions of many complex distributed algorithms. It also covers three microkernels used for UNIX-like distributed systems (Mach, Chorus & Amoeba).',
  },
  {
    title: 'A Quarter Century of UNIX',
    author: 'Peter H. Salus',
    year: '1994',
    image: '/assets/computers/quarter-century-unix.webp',
    description: 'A detailed account of the early days told by the people who lived them. If you want to learn how it all started (and sometimes how it all went wrong), this is the book to read. And you also get to see pictures of all the Great Ancients, including Biff the Dog.',
  },
];

export const VINTAGE_CDS: VintageCD[] = [
  { title: '4.4BSD Lite', year: 'June 1994', description: 'Complete 4.4BSD Lite source distribution with all AT&T files removed. This is where NetBSD, FreeBSD & OpenBSD come from.' },
  { title: 'BSDisc', year: 'November 1994', description: 'Complete source & binaries for NetBSD 1.0 and FreeBSD 2.0. As far as I know, this was the first CD release for both OSes.' },
  { title: 'FreeBSD 2.0.5', year: 'July 1995', description: 'Full distribution (sources & binaries) plus a live CD.' },
  { title: 'FreeBSD 2.2.5', year: 'November 1997', description: 'Full distribution (sources & binaries), plus a live CD and a copy of the CVS repository.' },
  { title: 'FreeBSD Toolkit', year: 'May 1999', description: 'FreeBSD 2.2, 3.1 & 4.0, plus a ton of packages. It was really time for the DVD-ROM to be invented :)' },
  { title: 'GNU — Free Software for UNIX', year: 'February 1996', description: '83 source packages, with pre-compiled binaries for SunOS 4.1.4 and Solaris 2.4. Emacs, gcc, g++, gdb, perl 4 & 5.' },
];

export const UNIX_PHILOSOPHY = 'The UNIX philosophy extends far beyond technology — it\'s a way of thinking about freedom, choice, and the power of simple, elegant solutions. This custom license plate combines New Hampshire\'s state motto "Live Free or Die" with UNIX, representing the deep connection between the UNIX philosophy and the open source movement.';
