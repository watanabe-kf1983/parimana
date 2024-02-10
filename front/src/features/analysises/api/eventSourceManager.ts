export class EventSourceManager {
    private url: string;
    private eventSource: EventSource | null = null;
  
    constructor(url: string) {
      this.url = url;
    }
  
    startListening(onMessage: (data: any) => void): void {
      this.eventSource = new EventSource(this.url);
  
      this.eventSource.onmessage = (event) => {
        onMessage(event.data);
      };
  
      this.eventSource.onerror = (error) => {
        console.error('EventSource failed:', error);
        this.stopListening();
      };
    }
  
    stopListening(): void {
      if (this.eventSource) {
        this.eventSource.close();
        this.eventSource = null;
      }
    }
  }
  