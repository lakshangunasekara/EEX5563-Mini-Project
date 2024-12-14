import tkinter as tk
from tkinter import messagebox

class MemoryManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Next Fit Memory Management Algorithm")
        
        # Memory and Process Storage
        self.memory_blocks = []
        self.processes = []
        self.memory_size = 0
        self.process_size = 0
        self.last_allocated_index = -1

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Frame for Memory Blocks
        self.memory_frame = tk.LabelFrame(self.root, text="Memory Blocks", padx=10, pady=10)
        self.memory_frame.grid(row=0, column=0, padx=20, pady=20)

        # Frame for Process Sizes
        self.process_frame = tk.LabelFrame(self.root, text="Processes", padx=10, pady=10)
        self.process_frame.grid(row=0, column=1, padx=20, pady=20)

        # Memory Block Size Input
        tk.Label(self.memory_frame, text="Memory Block Sizes (comma separated):").grid(row=0, column=0)
        self.memory_input = tk.Entry(self.memory_frame)
        self.memory_input.grid(row=1, column=0)
        
        # Process Size Input
        tk.Label(self.process_frame, text="Process Sizes (comma separated):").grid(row=0, column=0)
        self.process_input = tk.Entry(self.process_frame)
        self.process_input.grid(row=1, column=0)

        # Button to Add Memory Blocks
        self.add_memory_btn = tk.Button(self.memory_frame, text="Add Memory Blocks", command=self.add_memory_blocks)
        self.add_memory_btn.grid(row=2, column=0)

        # Button to Add Processes
        self.add_process_btn = tk.Button(self.process_frame, text="Add Processes", command=self.add_processes)
        self.add_process_btn.grid(row=2, column=0)

        # Allocate Memory Button
        self.allocate_btn = tk.Button(self.root, text="Allocate Memory", command=self.allocate_memory)
        self.allocate_btn.grid(row=1, column=0, columnspan=2, pady=10)

        # Allocation Result Area
        self.result_label = tk.Label(self.root, text="Allocation Results:")
        self.result_label.grid(row=2, column=0, columnspan=2)
        self.result_display = tk.Text(self.root, width=50, height=10)
        self.result_display.grid(row=3, column=0, columnspan=2)

    # Add memory block sizes for allocation
    def add_memory_blocks(self):
        try:
            # Get the memory block sizes
            self.memory_blocks = list(map(int, self.memory_input.get().split(',')))
            self.memory_size = sum(self.memory_blocks)
            self.update_result_display("Memory blocks updated - [" +self.memory_input.get()+"]")
        except ValueError:
            messagebox.showerror("Input Error", "Invalid memory block sizes.")

    # Add process sizes for allocation
    def add_processes(self):
        try:
            # Get the process sizes
            self.processes = list(map(int, self.process_input.get().split(',')))
            self.process_size = len(self.processes)
            self.update_result_display("Processes updated - [" + self.process_input.get()+"]")
        except ValueError:
            messagebox.showerror("Input Error", "Invalid process sizes.")

    # Allocate memory and display result
    def allocate_memory(self):
        if not self.memory_blocks or not self.processes:
            messagebox.showerror("Error", "Please define both memory blocks and processes first.")
            return

        allocation_result = self.next_fit_algorithm()
        self.update_result_display(allocation_result)

    # Function to allocate the processes
    def next_fit_algorithm(self):
        allocation_result = []
        current_block = self.last_allocated_index
        for process in self.processes:
            allocated = False
            while True:
                current_block = (current_block + 1) % len(self.memory_blocks)
                if self.memory_blocks[current_block] >= process:
                    self.memory_blocks[current_block] -= process
                    allocation_result.append(f"Process {process} allocated to Block {current_block+1} ({list(map(int, self.memory_input.get().split(',')))[current_block]})")
                    self.last_allocated_index = current_block
                    allocated = True
                    allocation_result.append(f"Remaining memory block sizes after allocation: \n{self.memory_blocks} \n")
                    break
                if current_block == self.last_allocated_index:
                    allocation_result.append(f"Process {process} could not be allocated (No space left).\n")
                    break
        return "\n".join(allocation_result)

    # Display results
    def update_result_display(self, message):
        self.result_display.delete(1.0, tk.END)
        self.result_display.insert(tk.END, message)

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryManagementApp(root)
    root.mainloop()
