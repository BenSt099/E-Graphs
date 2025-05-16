import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Installation',
    Svg: require('@site/static/img/arrow-down-circle.svg').default,
    description: (
      <>
       Lernen Sie, die nötigen Dependencies zu installieren und die Software zu starten. 
      </>
    ),
  },
  {
    title: 'Benutzung',
    Svg: require('@site/static/img/alphabet.svg').default,
    description: (
      <>
        Sie werden in der Lage sein, E-Graphs zu erstellen, Rewrite Rules anzuwenden und Equality Saturation durchzuführen.
      </>
    ),
  },
  {
    title: 'Tests',
    Svg: require('@site/static/img/bookmark-check.svg').default,
    description: (
      <>
        Die Software ist durch Unit-Tests abgedeckt. Die Dokumentation erklärt Ihnen, wie sie auszuführen sind.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}
        </Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
