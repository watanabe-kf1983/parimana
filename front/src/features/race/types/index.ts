export type RaceSelectorProps = {
  raceId: string;
  onSetRaceId: (input: string) => void;
};

export type Category = { id: string; name: string };
export type MeetingDay = { category: Category; course: Course; date: string };
export type Course = { id: string; name: string };
export type Calendar = Map<string, Course[]>;
export type Race = { id: string; name: string; meeting_day: MeetingDay };

export type CategorySelectorProps = {
  value?: string;
  items: Category[];
  onSetCategoryId: (input: string) => void;
};

export type DateSelectorProps = {
  value?: string;
  items: string[];
  onSetDate: (input: string) => void;
};

export type RaceOnDaySelectorProps = {
  raceId?: string;
  races: Race[];
  onSetRaceId: (input: string) => void;
};
