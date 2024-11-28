import * as React from "react";
import {
  Unstable_NumberInput as BaseNumberInput,
  NumberInputProps,
} from "@mui/base/Unstable_NumberInput";
import StyledInputRoot from "./styled-inputs/StyledInputRoot";
import StyledInputElement from "./styled-inputs/StyledInputElement";
import StyledButton from "./styled-inputs/StyledButton";

/**
 * Custom Number Input Component
 * Taken from https://mui.com/base-ui/react-number-input/
 */
const NumberInput = React.forwardRef(function CustomNumberInput(
  props: NumberInputProps,
  ref: React.ForwardedRef<HTMLDivElement>
) {
  return (
    <BaseNumberInput
      slots={{
        root: StyledInputRoot,
        input: StyledInputElement,
        incrementButton: StyledButton,
        decrementButton: StyledButton,
      }}
      slotProps={{
        incrementButton: {
          children: "▴",
        },
        decrementButton: {
          children: "▾",
        },
      }}
      {...props}
      ref={ref}
    />
  );
});

export default function CustomNumberInput({
  value,
  setValue,
}: {
  value: number | null;
  setValue: (val: number | null) => void;
}) {
  return (
    <NumberInput
      aria-label="Demo number input"
      placeholder="Type a number…"
      value={value}
      onChange={(_event, val) => setValue(val)}
    />
  );
}
