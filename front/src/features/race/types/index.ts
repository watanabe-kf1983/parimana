export type RaceSelectorProps = {
  raceId: string;
  onSetRaceId: (input: string) => void;
};

export type Category = { id: string; name: string };
export type Course = {
  id: string;
  name: string;
  category: Category;
};
export type Fixture = {
  category: Category;
  course: Course;
  date: string;
};
export type RaceInfo = { id: string; name: string; fixture: Fixture };
export type RaceSchedule = { course: Course; races: RaceInfo[] };
export type Calendar = { [date: string]: RaceSchedule[] };

export type CategorySelectorProps = {
  value?: string;
  items?: Category[];
  onChange: (input: string) => void;
};

export type DateSelectorProps = {
  value?: string;
  items?: string[];
  onChange: (input: string) => void;
};

export type CourseSelectorProps = {
  value?: string;
  items?: Course[];
  onChange: (input: string) => void;
};

export type RaceOnDaySelectorProps = {
  value?: string;
  items?: RaceInfo[];
  onChange: (input: string) => void;
};
