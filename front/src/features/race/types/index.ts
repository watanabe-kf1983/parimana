export type RaceSelectorProps = {
  raceId: string;
  onSetRaceId: (input: string) => void;
};

export type Category = { id: string; name: string };
export type MeetingDay = {
  category: Category;
  course: Course;
  date: string;
};
export type Course = { id: string; name: string };
export type Calendar = { [date: string]: { course: Course; races: Race[] }[] };
export type Race = { id: string; name: string };
export type RaceInfo = { id: string; name: string; meeting_day: MeetingDay };

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
  items?: Race[];
  onChange: (input: string) => void;
};
