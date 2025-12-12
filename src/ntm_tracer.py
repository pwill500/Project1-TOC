from src.helpers.turing_machine import TuringMachineSimulator


# ==========================================
# PROGRAM 1: Nondeterministic TM
# ==========================================
class NTM_Tracer(TuringMachineSimulator):
    def run(self, input_string, max_depth):
        """
        Performs a Breadth-First Search (BFS) trace of the NTM.
        Ref: Section 4.1 "Trees as List of Lists"
        """
        print(f"Tracing NTM: {self.machine_name} on input '{input_string}'")

        self.blank_symbol = '_'

        # Initial Configuration: ["", start_state, input_string]
        # Note: Represent configuration as triples (left, state, right)
        initial_config = [[], self.start_state, list(input_string)]

        # The tree is a list of lists of configurations
        tree = [[initial_config]]

        depth = 0
        accepted = False

        while depth < max_depth and not accepted:
            current_level = tree[-1]
            next_level = []
            all_rejected = True

            # TODO: STUDENT IMPLEMENTATION NEEDED
            # 1. Iterate through every config in current_level.
            if depth == 0:
                self.simulated_transitions = 0
                print("[", end="") # Start of the tree list

            # --- DISPLAY LOGIC: Mirror the image format (List of Lists of Triples) ---
            display_level = []
            for c in current_level:
                l_str = "".join(c[0]) if c[0] else ""
                r_str = "".join(c[2]) if c[2] else ""
                # Create triple: [left, state, right]
                display_level.append([l_str, c[1], r_str])
            
            # Print the current level as a list, adding a comma if not the first
            if depth > 0:
                print(",")
            print(f"{display_level}", end="")
            # -----------------------------------------------------------------------

            for config in current_level:
                # Unpack safely (handles both 3-item root and 4-item descendants)
                left, state, right = config[:3]

            # 2. Check if config is Accept (Stop and print success)
                if state == self.accept_state:
                    print("]") # Close the tree list
                    print(f'String accepted in {depth}')
                    print(f'Total transitions simulated: {self.simulated_transitions}')
                    
                    # Backtrack to reconstruct path
                    path = []
                    curr_node = config
                    while curr_node:
                        # Reconstruct string format for this node
                        p_left, p_state, p_right = curr_node[:3]
                        
                        # Format: "left", "state", "head+right"
                        left_str = "".join(p_left) if p_left else ""
                        right_str = "".join(p_right) if p_right else ""
                        
                        path.append(f'["{left_str}", "{p_state}", "{right_str}"]')
                        
                        # Move to parent (4th element if it exists)
                        curr_node = curr_node[3] if len(curr_node) > 3 else None

                    # Path is recorded Accept -> Start, so reverse it
                    for step in reversed(path):
                        print(step)

                    accepted = True
                    break
            # 3. Check if config is Reject (Stop this branch only)
                if state == self.reject_state:
                    continue
            # 4. If not Accept/Reject, find valid transitions in self.transitions.
                curr = (right[0],) if right else (self.blank_symbol,)
                valid = False


                for src, tr_list in self.transitions.items():
                    if src != state:
                        continue

                    for t in tr_list:
                        read_ch = t['read']
                        dst = t['next']
                        write_ch = t['write']
                        direction = t['move'][0]


                        if read_ch != curr:
                            continue

                        valid = True
                        all_rejected = False
                        self.simulated_transitions += 1

                        new_left = left.copy()
                        new_right = right.copy()

                        # Write to tape
                        if new_right:
                            new_right[0] = write_ch[0]
                        else:
                            new_right = [write_ch[0]]
            # 5. If no explicit transition exists, treat as implicit Reject.
            # 6. Generate children configurations and append to next_level.

                        if direction == 'R':
                            if new_right:
                                new_left.append(new_right[0])
                                new_right = new_right[1:] if len(new_right) > 1 else []
                            else:
                                new_left.append(self.blank_symbol)
                                new_right = []

                        elif direction == 'L':
                            if new_left:
                                new_right.insert(0, new_left.pop())
                            else:
                                new_right.insert(0, self.blank_symbol)

                        # Store parent (config) as 4th element for backtracking
                        next_config = (new_left, dst, new_right, config)
                        next_level.append(next_config)

                        # (Verbose print removed to match requested format)

                if not valid:
                    continue

            if accepted:
                return
            
            # Placeholder for logic:
            for i, nc in enumerate(next_level):
                nl, ns, nr = nc[:3]

            if not next_level and all_rejected:
                # TODO: Handle "String rejected" output
                print("]") # Close tree
                print(f"String rejected in {depth}")
                print(f"Total transitions simulated: {self.simulated_transitions}")
                break

            tree.append(next_level)
            depth += 1

        if depth >= max_depth:
            print("]") # Close tree if max depth reached
            print(f"Execution stopped after {max_depth} steps.")  #

    def print_trace_path(self, final_node):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2
        """
        pass