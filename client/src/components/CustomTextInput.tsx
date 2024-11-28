import * as React from "react";
import { InputBase, InputBaseComponentProps } from "@mui/material";
import StyledInputRoot from "./styled-inputs/StyledInputRoot";
import StyledInputElement from "./styled-inputs/StyledInputElement";

/**
 * Custom String Input Component
 * Taken from https://mui.com/base-ui/react-number-input/
 */
const StringInput = React.forwardRef(function CustomNumberInput(
  props: InputBaseComponentProps,
  ref: React.ForwardedRef<HTMLDivElement>
) {
  return (
    <InputBase
      slots={{
        root: StyledInputRoot,
        input: StyledInputElement,
      }}
      inputProps={props}
      ref={ref}
    />
  );
});

export default function CustomStringInput({
  value,
  setValue,
  placeholder,
}: {
  value: string;
  setValue: (val: string) => void;
  placeholder?: string;
}) {
  return (
    <StringInput
      aria-label="String Input"
      placeholder={placeholder ? placeholder : "Start Typing..."}
      value={value || ""}
      type="text"
      onChange={(event: React.ChangeEvent<HTMLInputElement>) =>
        setValue(event.target.value)
      }
    />
  );
}
