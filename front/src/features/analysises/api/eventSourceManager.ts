export class EventSourceManager {
  private url: string;
  private terminateMessage: string;
  private eventSource: EventSource | null = null;

  constructor(url: string, terminateMessage: string) {
    this.url = url;
    this.terminateMessage = terminateMessage;
  }

  startListening(onMessage: (data: any) => void, onTerminate: () => void): void {
    this.stopListening();

    const eventSource: EventSource = new EventSource(this.url);
    eventSource.onmessage = (event) => {
      const message: string = event.data;
      if (message !== this.terminateMessage) {
        onMessage(event.data);
      } else {
        this.stopListening();
        onTerminate();
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
