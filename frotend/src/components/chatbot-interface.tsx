"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Send, RefreshCw } from "lucide-react";

interface Message {
  id: string;
  type: "user" | "bot";
  content: string;
}

interface BotResponse {
  id: string;
  content: string;
}

const generateMockResponses = (): BotResponse[] => {
  const responses = [
    "Based on the data analysis, the optimal approach would be to implement a multi-tiered strategy.",
    "From a technical perspective, this requires careful consideration of scalability and performance.",
    "The research indicates that user engagement increases by 35% with this method.",
    "Industry best practices suggest integrating these components for maximum efficiency.",
    "Alternative solutions include leveraging cloud infrastructure for better resource management.",
    "Statistical models show a high correlation between these variables.",
    "The framework provides robust support for this use case.",
    "Recent studies demonstrate significant improvements in processing time.",
  ];
  
  return Array.from({ length: 4 }, (_, i) => ({
    id: `response-${Date.now()}-${i}`,
    content: responses[Math.floor(Math.random() * responses.length)],
  }));
};

export const ChatbotInterface = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [currentResponses, setCurrentResponses] = useState<BotResponse[]>([]);
  const [isWaitingForResponse, setIsWaitingForResponse] = useState(false);

  const handleSendMessage = () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      type: "user",
      content: input.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsWaitingForResponse(true);

    setTimeout(() => {
      const responses = generateMockResponses();
      setCurrentResponses(responses);
      setIsWaitingForResponse(false);
    }, 500);
  };

  const handleGenerateNewResponses = () => {
    setIsWaitingForResponse(true);
    setTimeout(() => {
      const responses = generateMockResponses();
      setCurrentResponses(responses);
      setIsWaitingForResponse(false);
    }, 500);
  };

  const handleSelectResponse = (response: BotResponse) => {
    const botMessage: Message = {
      id: response.id,
      type: "bot",
      content: response.content,
    };

    setMessages((prev) => [...prev, botMessage]);
    setCurrentResponses([]);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4 gap-4">
      <Card className="flex-1 flex flex-col">
        <CardHeader>
          <CardTitle>AI Chatbot</CardTitle>
        </CardHeader>
        <CardContent className="flex-1 flex flex-col gap-4 p-4">
          <ScrollArea className="flex-1 pr-4">
            <div className="flex flex-col gap-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${
                    message.type === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg px-4 py-2 ${
                      message.type === "user"
                        ? "bg-primary text-primary-foreground"
                        : "bg-muted"
                    }`}
                  >
                    {message.content}
                  </div>
                </div>
              ))}
              {isWaitingForResponse && (
                <div className="flex justify-start">
                  <div className="bg-muted rounded-lg px-4 py-2">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 rounded-full bg-foreground/50 animate-pulse" />
                      <div className="w-2 h-2 rounded-full bg-foreground/50 animate-pulse delay-150" />
                      <div className="w-2 h-2 rounded-full bg-foreground/50 animate-pulse delay-300" />
                    </div>
                  </div>
                </div>
              )}
            </div>
          </ScrollArea>

          {currentResponses.length > 0 && (
            <div className="border-t pt-4">
              <p className="text-sm font-medium mb-3">Select a response:</p>
              <div className="flex flex-col gap-2">
                {currentResponses.map((response, index) => (
                  <Button
                    key={response.id}
                    variant="outline"
                    className="justify-start text-left h-auto py-3 px-4"
                    onClick={() => handleSelectResponse(response)}
                  >
                    <span className="font-medium mr-2">{index + 1}.</span>
                    <span className="flex-1">{response.content}</span>
                  </Button>
                ))}
                <Button
                  variant="secondary"
                  className="mt-2"
                  onClick={handleGenerateNewResponses}
                  disabled={isWaitingForResponse}
                >
                  <RefreshCw className="w-4 h-4 mr-2" />
                  Give Another Response
                </Button>
              </div>
            </div>
          )}

          <div className="flex gap-2">
            <Input
              placeholder="Type your message..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isWaitingForResponse || currentResponses.length > 0}
            />
            <Button
              onClick={handleSendMessage}
              disabled={!input.trim() || isWaitingForResponse || currentResponses.length > 0}
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

