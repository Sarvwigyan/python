import os
import torch
from transformers import AutoProcessor, AutoModelForCausalLM
from colorama import init, Fore
import speech_recognition as sr
import pyttsx3
from qiskit import QuantumCircuit

# Initialize Colorama for colored cmd output
init()

# Initialize Llama 4 Scout
model_id = "meta-llama/Llama-4-Scout-17B-16E-Instruct"
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    load_in_4bit=True  # Quantization for consumer GPU
)

# Initialize voice interaction
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    """Speak response using text-to-speech."""
    engine.say(text)
    engine.runAndWait()

def process_command(command, image_path=None):
    """Process text or multimodal input with Llama 4 Scout."""
    messages = [{"role": "user", "content": []}]
    
    # Add text to prompt
    messages[0]["content"].append({"type": "text", "text": command})
    
    # Add image if provided
    if image_path:
        messages[0]["content"].append({"type": "image", "url": image_path})
    
    # Prepare inputs
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_tensors="pt"
    ).to(model.device)
    
    # Generate response
    outputs = model.generate(**inputs, max_new_tokens=256)
    response = processor.batch_decode(outputs, skip_special_tokens=True)[0]
    return response

def simulate_hardware_control(action):
    """Simulate quantum hardware control on Windows."""
    if "adjust" in action.lower():
        return "Simulating adjustment of Faraday rotator on quantum hardware."
    return "Unknown hardware command."

def main():
    print(Fore.CYAN + "JARVIS: Ready to assist with your quantum computer project." + Fore.RESET)
    while True:
        try:
            # Voice input
            with sr.Microphone() as source:
                print(Fore.YELLOW + "Speak your command (or type 'exit'):" + Fore.RESET)
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio)
                print(Fore.BLUE + f"Command: {command}" + Fore.RESET)
        except sr.WaitTimeoutError:
            print(Fore.RED + "No speech detected. Try again." + Fore.RESET)
            continue
        except sr.UnknownValueError:
            print(Fore.RED + "Could not understand audio. Try again." + Fore.RESET)
            continue
        except KeyboardInterrupt:
            print(Fore.RED + "Exiting JARVIS." + Fore.RESET)
            break
        
        if command.lower() == "exit":
            break
        
        # Process quantum-related commands
        if "quantum circuit" in command.lower():
            response = process_command("Generate a Qiskit circuit for a 2-qubit entangled state.")
            print(Fore.GREEN + "Response: " + response + Fore.RESET)
            speak(response)
            # Example circuit output
            qc = QuantumCircuit(2, 2)
            qc.h(0)
            qc.cx(0, 1)
            qc.measure([0, 1], [0, 1])
            print(Fore.GREEN + str(qc) + Fore.RESET)
        
        # Simulate hardware control
        elif "adjust" in command.lower():
            response = simulate_hardware_control(command)
            print(Fore.GREEN + "Response: " + response + Fore.RESET)
            speak(response)
        
        # Process image (e.g., detector output)
        elif "image" in command.lower():
            image_path = input(Fore.YELLOW + "Enter image path or URL (e.g., C:\\detector_output.jpg): " + Fore.RESET)
            response = process_command("Describe this quantum detector output.", image_path)
            print(Fore.GREEN + "Response: " + response + Fore.RESET)
            speak(response)
        
        else:
            response = process_command(command)
            print(Fore.GREEN + "Response: " + response + Fore.RESET)
            speak(response)

if __name__ == "__main__":
    main()