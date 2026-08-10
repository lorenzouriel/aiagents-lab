# Agent Voice Retell AI
A voice assistant implementation for Retell AI, designed to provide automated customer service for e-commerce stores. This project includes bilingual support (English and Portuguese) with customizable prompts and knowledge bases.

## Overview
This repository contains prompt templates and knowledge base files for creating intelligent voice assistants powered by Retell AI. The assistant is configured to handle customer inquiries, product information, order tracking, and seamless handoffs to human agents when needed.

## Project Structure
```bash
agent-voice-retellai/
├── en-prompts/           # English language prompts
│   ├── universal.md      # Main system prompt and persona
│   ├── custom_message.md # Custom message templates
│   └── promtp-tree.md    # Prompt tree graph structure
│
├── pt-prompts/           # Portuguese language prompts
│   ├── universal.md      # Main system prompt and persona
│   ├── custom_message.md # Custom message templates
│   └── promtp-tree.md    # Prompt tree graph structure
│
└── data/                 # Knowledge base files
    ├── kb-en.md          # English product catalog
    └── kb-pt.md          # Portuguese product catalog
```

## Features

### Bilingual Support
- **English** (en-prompts)
- **Portuguese** (pt-prompts)

### Core Capabilities
- Product search and recommendations
- Stock availability checking
- Order tracking assistance
- Payment and shipping information
- FAQ responses
- Smart handoff to human agents
- Privacy-conscious data handling

### Assistant Personality
- Welcoming and friendly tone
- Professional yet approachable
- Clear and concise communication
- Natural conversation flow
- Patient and respectful interaction style

## Use Cases

The voice assistant is designed to handle:

1. **Product Inquiries**
   - Finding specific products
   - Checking availability
   - Providing product details and ingredients
   - Offering personalized recommendations

2. **Order Management**
   - Tracking orders
   - Calculating shipping costs
   - Processing exchanges and returns
   - Managing cart operations

3. **Customer Support**
   - Answering frequently asked questions
   - Explaining payment methods
   - Providing delivery information
   - Handling complaints with empathy

4. **Human Handoff**
   - Identifying when human intervention is needed
   - Seamless transfer to WhatsApp or human agents
   - Collecting necessary information before transfer

## Prompt Structure

### Universal Prompt
The universal prompt ([universal.md](en-prompts/universal.md)) defines:
- System persona and guardrails
- Conversation style and tone
- Privacy and security protocols
- Example Q&A scenarios

### Prompt Tree
The prompt tree ([promtp-tree.md](en-prompts/promtp-tree.md)) organizes prompts into logical categories:
- **Introduction** - Greeting and context setting
- **Stock** - Availability inquiries
- **FAQ** - Common questions
- **Human Contact** - Transfer protocols

### Knowledge Base
Product catalog with:
- Complete product listings
- Prices and availability
- Ingredients and composition
- Usage instructions
- Product status tracking

## Configuration for Retell AI

### Setting Up Your Agent

1. **Upload Universal Prompt**
   - Use the content from `universal.md` as your main system prompt
   - Choose the language version (en/pt) based on your target audience

2. **Configure Knowledge Base**
   - Upload the corresponding `kb-*.md` file to provide product information
   - Update product details, prices, and availability as needed

3. **Implement Prompt Tree**
   - Structure your conversation flow using the prompt tree graph
   - Customize prompts for your specific business needs

### Customization

To adapt this for your business:

1. **Update Brand Information**
   - Replace "VAIB" with your brand name
   - Adjust the product category descriptions
   - Modify the tone to match your brand voice

2. **Customize Product Catalog**
   - Edit the knowledge base files with your products
   - Update pricing, availability, and descriptions
   - Add or remove product categories as needed

3. **Adjust Conversation Flow**
   - Modify example Q&A pairs to match common customer questions
   - Add specific policies (return policy, shipping rules, etc.)
   - Configure payment methods and shipping options

## Example Conversations

### Product Search
```
User: "Hi"
Assistant: "Hello! Welcome to VAIB — handcrafted cosmetics made with care.
How can I help you today? Do you want to search for a product,
ask questions, or check an order?"
```

### Stock Inquiry
```
User: "Do you have a body scrub for dry skin?"
Assistant: "Yes — we have a scrub indicated for dry skin that leaves
the skin soft and well-hydrated. Would you like me to tell you
the ingredients and how to use it?"
```

### Human Handoff
```
User: "I want to speak with a human agent"
Assistant: "Sure — no problem. I can transfer you to our human
support team via WhatsApp. Would you like me to send a message
now so we can start the service?"
```

## Best Practices

### Privacy and Security
- Never request sensitive data unnecessarily
- Explain why information is needed before asking
- Direct users to secure channels for sensitive operations
- Maintain customer confidentiality

### Conversation Quality
- Keep responses concise and natural
- Use natural pauses in speech
- Avoid technical jargon
- Be patient with unclear requests
- Offer alternatives when something isn't possible

### Guardrails
- Politely decline unsupported operations
- Offer alternatives instead of just saying "no"
- Know when to escalate to human support
- Stay within defined scope and capabilities

## Languages

- **English**: Full support with example prompts for international markets
- **Portuguese (Brazilian)**: Localized prompts with local payment methods (PIX, boleto)

## Contributing

To improve or extend this voice assistant:

1. Update prompts in the appropriate language folder
2. Maintain consistency across bilingual versions
3. Test conversation flows thoroughly
4. Keep knowledge bases synchronized with actual inventory

## Use Case Example

This implementation is configured for **VAIB**, a handcrafted cosmetics brand, but can be adapted for:
- E-commerce stores
- Service businesses
- Appointment scheduling
- Customer support hotlines
- Product information lines
