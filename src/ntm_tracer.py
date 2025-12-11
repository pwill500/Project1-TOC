from src.helpers.turing_machine import TuringMachineSimulator


# ==========================================
# PROGRAM 1: Nondeterministic TM [cite: 137]
# ==========================================
class NTM_Tracer(TuringMachineSimulator):
    def run(self, input_string, max_depth):
        """
        Performs a Breadth-First Search (BFS) trace of the NTM.
        Ref: Section 4.1 "Trees as List of Lists" [cite: 146]
        """
        print(f"Tracing NTM: {self.machine_name} on input '{input_string}'")

        self.blank_symbol = '_'

        # Initial Configuration: ["", start_state, input_string]
        # Note: Represent configuration as triples (left, state, right) [cite: 156]
        initial_config = [[], self.start_state, list(input_string) + [self.blank_symbol]]

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
            for config in current_level:
                left, state, right = config

            # 2. Check if config is Accept (Stop and print success) [cite: 179]
                if state == self.accept_state:
                    print(f'string accepted: depth = {depth}. path to acceptance: {config}')
                    accepted = True
                    break
            # 3. Check if config is Reject (Stop this branch only) [cite: 181]
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

                        new_left = left.copy()
                        new_right = right.copy()

                        # Write to tape
                        if new_right:
                            new_right[0] = write_ch[0]
                        else:
                            new_right = [write_ch[0]]
            # 5. If no explicit transition exists, treat as implicit Reject.
            # 6. Generate children configurations and append to next_level[cite: 148].

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

                        next_config = (new_left, dst, new_right)
                        next_level.append(next_config)

                if not valid:
                    continue

            if accepted:
                return

            if not next_level and all_rejected:
                # TODO: Handle "String rejected" output [cite: 258]
                print("String rejected")
                break

            tree.append(next_level)
            depth += 1

        if depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")  # [cite: 259]

    def print_trace_path(self, final_node):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """
        pass
