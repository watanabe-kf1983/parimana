export class EventSourceManager {
  private url: string;
  private terminateMessage: string;
  private abortMessage: string;
  private eventSource: EventSource | null = null;

  constructor(url: string, terminateMessage: string, abortMessage: string) {
    this.url = url;
    this.terminateMessage = terminateMessage;
    this.abortMessage = abortMessage;
  }

  startListening(onMessage: (data: any) => void, onTerminate: () => void, onAbort: () => void): void {
    this.stopListening();

    const eventSource: EventSource = new EventSource(this.url);
    eventSource.onmessage = (event) => {
      const message: string = event.data;
      if (message === this.terminateMessage) {
        this.stopListening();
        onTerminate();
      } else if (message === this.abortMessage) {
        this.stopListening();
        onAbort();
      } else {
        onMessage(event.data);
      }
    };
    eventSource.onerror = (error) => {
      if (eventSource.readyState === EventSource.CLOSED) {
        console.log('Connection was closed or failed.');
      }
      console.error('EventSource failed:', error);
      this.stopListening();
    };

    this.eventSource = eventSource
  }

  stopListening(): void {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
  }
}
