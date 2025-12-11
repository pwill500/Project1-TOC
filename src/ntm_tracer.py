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
        print("ACCEPT STATE LOADED AS:", self.accept_state)

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

                print(f"EXPAND depth={depth} config=({''.join(left) if left else ''}, {state}, {''.join(right) if right else ''})")

            # 2. Check if config is Accept (Stop and print success) [cite: 179]
                if state == self.accept_state:
                    print(f'string accepted: depth = {depth}. path to acceptance: {config}')
                    accepted = True
                    break
            # 3. Check if config is Reject (Stop this branch only) [cite: 181]
                if state == self.reject_state:
                    print(f"  branch at state {state} is explicit reject; skipping")
                    continue
            # 4. If not Accept/Reject, find valid transitions in self.transitions.
                curr = (right[0],) if right else (self.blank_symbol,)
                valid = False

                print(f"  read_symbol (tuple) = {curr}")

                for src, tr_list in self.transitions.items():
                    if src != state:
                        continue

                    for t in tr_list:
                        read_ch = t['read']
                        dst = t['next']
                        write_ch = t['write']
                        direction = t['move'][0]

                        print(f"    candidate: (state={src}, read={read_ch}, next={dst}, write={write_ch}, move={t['move']})")

                        if read_ch != curr:
                            print("      -> read mismatch")
                            continue

                        valid = True
                        all_rejected = False
                        print(f"      -> MATCH: will transition to {dst} writing {write_ch} moving {direction}")

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

                            print(f"        produced child: ({''.join(new_left) if new_left else ''}, {dst}, {''.join(new_right) if new_right else ''})")

                if not valid:
                    print(f"  no valid transitions from ({''.join(left) if left else ''}, {state}, {''.join(right) if right else ''})")
                    continue

            if accepted:
                return
            
            # Placeholder for logic:
            print(f"AFTER depth={depth} produced {len(next_level)} next configs:")
            for i, nc in enumerate(next_level):
                nl, ns, nr = nc
                print(f"  next[{i}]=({''.join(nl) if nl else ''}, {ns}, {''.join(nr) if nr else ''})")

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
