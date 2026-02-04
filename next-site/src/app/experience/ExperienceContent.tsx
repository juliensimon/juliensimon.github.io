'use client';

import { motion } from 'framer-motion';

import { EXPERIENCES, EDUCATION } from '@/data/experience';

export default function ExperienceContent() {
  return (
    <>
      <div className="pt-24 pb-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold font-heading text-text">
          Experience
        </h1>
        <p className="mt-2 text-text-muted">
          30+ years of research-informed technology leadership — from embedded systems to AI at scale
        </p>
      </div>

      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        {/* Timeline */}
        <div className="relative">
          {/* Vertical line */}
          <div className="absolute left-0 md:left-1/2 top-0 bottom-0 w-px bg-gradient-to-b from-primary via-secondary to-highlight" />

          {EXPERIENCES.map((exp, i) => {
            const isLeft = i % 2 === 0;
            return (
              <motion.div
                key={`${exp.company}-${exp.period}`}
                initial={{ opacity: 0, x: isLeft ? -30 : 30 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true, margin: '-50px' }}
                transition={{ duration: 0.5, delay: 0.1 }}
                className={`relative mb-12 md:w-[calc(50%-2rem)] ${
                  isLeft ? 'md:mr-auto md:pr-8' : 'md:ml-auto md:pl-8'
                } pl-8 md:pl-0`}
              >
                {/* Dot on timeline */}
                <div className="absolute left-[-5px] md:left-auto top-2 w-3 h-3 rounded-full bg-primary shadow-lg shadow-primary/30 md:hidden" />
                <div
                  className={`hidden md:block absolute top-2 w-3 h-3 rounded-full bg-primary shadow-lg shadow-primary/30 ${
                    isLeft ? 'right-[-7px]' : 'left-[-7px]'
                  }`}
                />

                <div className="glass-card rounded-xl p-6">
                  <p className="text-xs font-medium text-highlight mb-1">{exp.period}</p>
                  <h3 className="text-lg font-bold font-heading text-text">
                    {exp.title}
                  </h3>
                  <p className="text-sm font-semibold text-primary mb-2">
                    {exp.companyUrl ? (
                      <a href={exp.companyUrl} target="_blank" rel="noopener noreferrer" className="hover:underline">
                        {exp.company}
                      </a>
                    ) : (
                      exp.company
                    )}
                  </p>
                  <p className="text-sm text-text-muted mb-3">
                    {exp.description}
                  </p>

                  {exp.achievements && (
                    <ul className="space-y-1 mb-3">
                      {exp.achievements.map((a, j) => (
                        <li key={j} className="text-xs text-text-muted flex gap-2">
                          <span className="text-primary mt-0.5 shrink-0">&#8226;</span>
                          <span>{a}</span>
                        </li>
                      ))}
                    </ul>
                  )}

                  {exp.techEnvironment && (
                    <div className="flex flex-wrap gap-1.5 mt-3 pt-3 border-t border-border">
                      {exp.techEnvironment.flatMap((te) =>
                        te.items.map((item) => (
                          <span
                            key={item}
                            className="text-[10px] px-2 py-0.5 rounded-full bg-primary/10 text-primary font-medium"
                          >
                            {item}
                          </span>
                        ))
                      )}
                    </div>
                  )}
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* Education */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-16"
        >
          <h2 className="text-2xl font-bold font-heading gradient-brand-text mb-6 text-center">
            Education
          </h2>
          <div className="grid sm:grid-cols-2 gap-4 max-w-2xl mx-auto">
            {EDUCATION.map((edu) => (
              <div
                key={edu.degree}
                className="glass-card rounded-xl p-5 text-center"
              >
                <p className="text-base font-semibold text-text">{edu.degree}</p>
                <p className="text-sm text-text-muted">{edu.school}</p>
                <p className="text-xs text-highlight mt-1">{edu.year}</p>
              </div>
            ))}
          </div>
        </motion.div>
      </section>
    </>
  );
}
