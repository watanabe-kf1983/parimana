export type RaceSelectorProps = {
  initialRaceId?: string;
  showControl: boolean;
  onClearRaceId: () => void;
  onSetInitialRaceId: (input: string | undefined) => void;
};

export type Category = { id: string; name: string };
export type Course = {
  id: string;
  name: string;
  category: Category;
};
export type Fixture = {
  course: Course;
  date: string;
};
export type RaceInfo = { id: string; name: string; fixture: Fixture };
