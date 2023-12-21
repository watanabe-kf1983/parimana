import { RaceProps } from '../types';
import { Analysis } from './Analysis';

export function RaceAnalysises(props: RaceProps) {

  return (
    <>
      <Analysis raceId={props.raceId} modelName="no_cor" />
    </>
  )
}
