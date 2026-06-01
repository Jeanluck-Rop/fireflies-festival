import { zxcvbn, type Match } from "@zxcvbn-ts/core";

export interface PasswordStrength {
  pct: number;
  label: string;
  color: string;
}

const STRENGTH_MAP: PasswordStrength[] = [
  { pct: 25, label: 'Muy Débil', color: '#FF8A7B' },
  { pct: 40, label: 'Débil', color: '#FFB87B' },
  { pct: 60, label: 'Aceptable', color: '#E8FF7A' },
  { pct: 80, label: 'Buena', color: '#7BD8B0' },
  { pct: 100, label: 'Excelente', color: '#7BD882' },
];

function getEmailData(email: string) {
  const emailUser = email.split('@')[0] || '';
  const emailClean = emailUser.toLowerCase().replace(/[^a-zA-Z0-9]/g, '');

  return {emailUser, emailClean};
}

export function getPasswordStrength(password: string, email: string = ''): PasswordStrength {
  const p = password || '';
  const { emailUser, emailClean } = getEmailData(email);

  if (!p || p.length < 8) {
    return { pct: 0, label: '—', color: '#5C645F' };
  }
  if (/^\d+$/.test(p)) {
    return { pct: 25, label: 'Muy Débil', color: '#FF8A7B' };
  }

  const result = zxcvbn(p, [email, emailUser, emailClean]);
  const score = result.score;
  const pClean = p.toLowerCase().replace(/[^a-zA-Z0-9]/g, '');
  const emailWithoutNumbers = emailClean.replace(/[0-9]/g, '');
  if (emailWithoutNumbers && pClean.includes(emailWithoutNumbers)) {
    return { pct: 25, label: 'Muy Débil', color: '#FF8A7B' };
  }

  return STRENGTH_MAP[score];
}

export function validatePassword(password: string, email: string = ''): string {
  if (!password) {
    return 'La contraseña es requerida';
  }
  if (password.length < 8) {
    return 'Mínimo 8 caracteres';
  }
  if (/^\d+$/.test(password)) {
    return 'La contraseña no puede contener solo números';
  }
  if (!/[A-Z]/.test(password)) {
    return 'Debe incluir al menos una mayúscula';
  }
  if (!/[a-z]/.test(password)) {
    return 'Debe incluir al menos una minúscula';
  }
  if (!/[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(password)) {
    return 'Debe incluir al menos un símbolo';
  }
  if (!/\d/.test(password)) {
    return 'Debe incluir al menos un número';
  }

  const { emailUser, emailClean } = getEmailData(email);
  const result = zxcvbn(password, [email, emailUser, emailClean]);

  if (result.score < 2) {
    const matchesEmail = result.sequence.some(
      (seq: Match) => seq.dictionaryName === 'user_inputs'
    );

    if (matchesEmail) {
      return 'La contraseña no puede ser similar a tu correo electrónico';
    }

    return 'La contraseña es demasiado común o fácil de adivinar';
  }

  const pClean = password.toLowerCase().replace(/[^a-zA-Z0-9]/g, '');
  const emailWithoutNumbers = emailClean.replace(/[0-9]/g, '');

  if (emailWithoutNumbers && pClean.includes(emailWithoutNumbers)) {
    return 'La contraseña no puede ser similar a tu correo electrónico';
  }

  const passStrength = getPasswordStrength(password, email);
  if (passStrength.pct < 60) {
    return `La contraseña es demasiado débil. ${passStrength.label}`;
  }

  return '';
}